# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import signal
import codecs
import datetime
import hashlib
import logging
import os
import re
import sqlite3
from urlparse import urlparse
import json

import requests
import tldextract
from bs4 import BeautifulSoup


class TimeoutError(Exception): pass


def timeout_wrapper(seconds, other_thing):
    def _wapper(func):
        def timeout_handler(signum, frame):
            other_thing()
            signal.alarm(seconds)

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(seconds)

        return func

    return _wapper


def do_other_thing():
    return


def list2str(l):
    """
    列表转字符串
    :param l:
    :return:
    """
    st_list = []
    for i in l:
        item = "\t".join(i)
        st_list.append(item)
    return os.linesep.join(st_list)


def path(*paths):
    """
    :param paths:
    :return:
    """
    MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
    # ROOT_PATH = os.path.join(MODULE_PATH, os.path.pardir)
    return os.path.abspath(os.path.join(MODULE_PATH, *paths))


def parse_url(url, isupdate=False):
    """
    url解析
    :param url:
    :return:
    """
    o = urlparse(url)
    extract = tldextract.TLDExtract()
    if isupdate:
        extract.update()
    ext = extract(url)
    return [o, ext]


def strip_n(st):
    """

    :param st:
    :return:
    """
    if not st:
        return st

    st = re.sub(r'\n', ' ', st)
    st = re.sub(r'\s+', ' ', st)
    st = re.sub(r'\x22', '', st)
    st = re.sub(r'\x27', '', st)

    st = st.strip()
    return st


class SQLiteOper(object):
    """

    """

    def __init__(self, dbpath="", db_is_new=False, schemafile=""):
        if db_is_new:
            print("create new schema")
            if os.path.exists(dbpath):
                os.remove(dbpath)
            with codecs.open(schemafile, mode='rb', encoding='utf-8', errors='ignore') as f:
                schema = f.read()
                self.sqlite3_conn = sqlite3.connect(dbpath, timeout=20)
                self.executescript(schema)
        self.sqlite3_conn = sqlite3.connect(dbpath, timeout=20)

    def __del__(self):
        self.sqlite3_conn.close()

    def executescript(self, sql_script):
        self.sqlite3_conn.executescript(sql_script)

    def query(self, query_statement, operate_dict=None):
        """
        select statement
        :param query:
        :return:
        """

        logging.debug(query_statement)
        cursor = self.sqlite3_conn.cursor()
        if operate_dict is not None:
            cursor.execute(query_statement, operate_dict)
        else:
            cursor.execute(query_statement)

        for line in cursor.fetchall():
            yield line

    def executemany(self, operate_statement, operate_list=None):
        """insert/update"""
        logging.debug(operate_statement)
        cursor = self.sqlite3_conn.cursor()

        cursor.executemany(operate_statement, operate_list)

        self.sqlite3_conn.commit()

    def execute(self, sql):
        """

        :param sql:
        :return:
        """
        logging.debug(sql)
        cursor = self.sqlite3_conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            logging.error("[execute_failed]: sql(%s) e(%s)" % (sql, str(e)))

        self.sqlite3_conn.commit()


def get_special_date(delta=0, format="%Y%m%d"):
    """
    now 20160918, default delata = 0
    :return:
    """
    date = (datetime.date.today() + datetime.timedelta(days=delta)).strftime(format)
    return date


def get_weixin_info(url="", ts="", tag="", max_redirects=30, proxy=None, root_dir="data/weixin", retry=3, timeout=10):
    """
    微信解析
    :param url:
    :param max_redirects:
    :param proxy:
    :param root_dir:
    :return:
    """
    root_dir = path(root_dir)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    hl = hashlib.md5()
    hl.update(url.encode(encoding='utf-8'))

    fname = path(root_dir, "%s.html" % hl.hexdigest())

    if not os.path.exists(fname):
        get_request(url, proxy=proxy, fname=fname, retry=retry, max_redirects=max_redirects, timeout=timeout)

    if os.path.exists(fname):
        with codecs.open(fname, mode='rb') as fr:
            try:
                soup = BeautifulSoup(fr, 'lxml')

            except Exception as e:
                logging.error("GET title of %s failed : %s" % (url, repr(e)))
                return

            title = soup.find('h2', class_="rich_media_title")
            if title:
                title = title.text
                if title:
                    title = strip_n(title)

            rich_media_meta_list = soup.find("div", class_="rich_media_meta_list")

            nickname_chineses = ""
            nickname_english = ""
            weixin_no = ""
            weixin_subject = ""

            if rich_media_meta_list:
                media_meta_text = rich_media_meta_list.find("span", class_="rich_media_meta rich_media_meta_text")

                if media_meta_text:
                    nickname_chineses = media_meta_text.text

                profile_inner = rich_media_meta_list.find("div", class_="profile_inner")

                if profile_inner:
                    weixin_no = profile_inner.find("strong", class_="profile_nickname")
                    if weixin_no:
                        nickname_english = weixin_no.text

                    profile_metas = profile_inner.find_all("span", class_="profile_meta_value")

                    if profile_metas:
                        if len(profile_metas) == 2:
                            weixin_no = profile_metas[0].text
                            weixin_subject = profile_metas[1].text

            if not nickname_english:
                return

            overview = {
                'nickname_english': strip_n(nickname_english),
                'nickname_chinese': strip_n(nickname_chineses),
                'url': strip_n(url),
                'weixin_no': strip_n(weixin_no),
                'weixin_subject': strip_n(weixin_subject),
                'title': strip_n(title),
                'ts': ts,
                'tag': tag

            }

            return overview


def get_github_info(url="", title="", ts="", tag="",
                    max_redirects=30, proxy=None, root_dir="data/githubcom", isnew=False,
                    retry=3, timeout=10):
    """
    github解析
    :param url:
    :param max_redirects:
    :param proxy:
    :param root_dir:
    :return:
    """
    file_404 = path("data/github_404")
    urls_404 = set()
    if os.path.exists(file_404):

        with codecs.open(file_404, mode='rb') as fr:
            for line in fr:
                line = line.strip()
                if line:
                    urls_404.add(line)

    pattern = "(https://github.com/([^/]+))"
    match = re.search(pattern, url)
    overview = {}
    overview['title'] = strip_n(title)
    overview["url"] = url
    overview['ts'] = ts
    overview['tag'] = tag
    if match:
        url_root, github_id = match.groups()

        overview["github_id"] = github_id

        if url_root in urls_404:
            return
    else:
        return

    root_dir = path(root_dir)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

    hl = hashlib.md5()
    hl.update(url.encode(encoding='utf-8'))

    fname = path(root_dir, "%s.html" % hl.hexdigest())

    if isnew or not os.path.exists(fname):
        get_request(url_root, proxy=proxy, fname=fname, fname_404=file_404, retry=retry,
                    timeout=timeout, max_redirects=max_redirects)

    if os.path.exists(fname):
        with codecs.open(fname, mode='rb') as fr:
            try:
                soup = BeautifulSoup(fr, 'lxml')
            except Exception as e:
                logging.error("GET title of %s failed : %s" % (url, repr(e)))
                return

            # 1. find org-description
            org_sub = soup.find("p", class_='org-description')
            if org_sub:
                org_sub = org_sub.next_sibling
                if org_sub:
                    org_sub = org_sub.get_text()
                    org_sub = strip_n(org_sub)

            overview["org_profile"] = org_sub

            # 2. find geo and url

            org_meta = soup.find("ul", class_=re.compile("org-header-meta"))
            org_url = None
            org_geo = None
            if org_meta:
                org_url = org_meta.find("a")
                if org_url:
                    org_url = strip_n(org_url.get("href"))

                org_geo = org_meta.find("li", class_=re.compile('meta-item v-align-middle'))
                if org_geo:
                    org_geo = strip_n(org_geo.get_text())

            overview["org_url"] = org_url
            overview["org_geo"] = org_geo

            # 3.  repos#people#project
            for aa in soup.find_all("a", class_=re.compile(r'pagehead-tabs-item')):
                aa = aa.get_text()
                aa = strip_n(aa)
                if aa:
                    parts = re.split("\s+", aa)

                    if len(parts) == 2:
                        t = re.sub(',', '.', parts[1])

                        p = re.match('(\d+\.*\d*)([km]*)', t)
                        if p:
                            n, d = p.groups()

                            if d == 'k':
                                t = float(n) * 1000
                            elif d == 'm':
                                t = float(n) * 1000000
                            else:
                                pos = n.find('.')
                                if pos != -1:
                                    t = int(float(n) * pow(10, len(n[n.find('.') + 1:])))

                        overview["org_%s" % parts[0].lower()] = t

            # 4. star forks
            overview["repo_star"] = 0
            overview["repo_forks"] = 0
            repo_language = set()

            # repo
            for aa in soup.find_all('span', class_=re.compile('repo-language-color')):
                aa_p = aa.parent
                if aa_p:
                    aa_p = strip_n(aa_p.get_text())
                    if aa_p:
                        p = re.split(r'\s+', aa_p)
                        if len(p) > 0:
                            repo_language.add(p[0])
            if repo_language:
                repo_language = ",".join(repo_language)
            else:
                repo_language = ""

            overview["repo_lang"] = repo_language

            for aa in soup.find_all("a", class_="pinned-item-meta muted-link"):

                t = strip_n(aa.get_text())

                if re.match('^\d+$', t):
                    t = int(t)
                else:
                    t = re.sub(',', '.', t)
                    p = re.match('(\d+\.*\d*)([km])', t)
                    if p:
                        n, d = p.groups()

                        if d == 'k':
                            t = float(n) * 1000
                        elif d == 'm':
                            t = float(n) * 1000000
                        else:
                            t = int(n)
                    else:
                        continue

                star = aa.find("svg", class_="octicon octicon-star")
                if star:
                    if t > overview["repo_star"]:
                        overview["repo_star"] = t
                else:
                    forks = aa.find("svg", class_="octicon octicon-repo-forked")
                    if forks:
                        if t > overview["repo_forks"]:
                            overview["repo_forks"] = t

            # 5. languages
            overview["org_lang"] = []
            for aa in soup.find_all("a", class_="no-wrap text-gray d-inline-block muted-link mt-2"):
                t = strip_n(aa.get_text())
                overview["org_lang"].append(t)

            overview["org_lang"] = ",".join(overview["org_lang"])

            overview["github_type"] = 1  # 1: org 0:private
            if not (org_sub or org_geo or org_url):
                overview["github_type"] = 0

                # repos #stars #followers#following
                for aa in soup.find_all("a", class_=re.compile('UnderlineNav-item')):
                    aa = aa.get_text()
                    aa = strip_n(aa)
                    if aa:
                        parts = re.split("\s+", aa)

                        if len(parts) == 2:
                            t = re.sub(',', '.', parts[1])
                            p = re.match('(\d+\.*\d*)([km]*)', t)
                            if p:
                                n, d = p.groups()

                                if d == 'k':
                                    t = int(float(n) * 1000)
                                elif d == 'm':
                                    t = int(float(n) * 1000000)
                                else:
                                    t = int(n)
                            overview["p_%s" % parts[0].lower()] = t

                # 个人简介
                p_profile = soup.find("div", class_=re.compile("p-note user-profile-bio"))
                if p_profile:
                    p_profile = strip_n(p_profile.get_text())

                overview["p_profile"] = p_profile

                # 公司
                p_company = soup.find("span", class_=re.compile("p-org"))
                if p_company:
                    p_company = strip_n(p_company.get_text())

                overview["p_company"] = p_company

                # 地理位置
                p_loc = soup.find("span", class_=re.compile("p-label"))
                if p_loc:
                    p_loc = strip_n(p_loc.get_text())

                overview["p_loc"] = p_loc

                # url
                p_url = soup.find("div", class_=re.compile('js-profile-editable-area'))

                if p_url:
                    p_url = p_url.find_all("a")

                    if p_url:
                        for p_url_i in p_url:
                            p_url_i = p_url_i.get("href")
                            if p_url_i.startswith("http"):
                                p_url = p_url_i
                                break
                            else:
                                p_url = ""

                if not p_url:
                    p_url = None

                overview["p_url"] = strip_n(p_url)

                # organizations
                github_org = soup.find("a", class_='avatar-group-item')
                if github_org:
                    github_org = github_org.get("href")

                overview["p_github_org"] = strip_n(github_org)
                if 'p_packages' in overview:
                    del overview['p_packages']

    return overview


@timeout_wrapper(1, do_other_thing)
def get_request(url,
                max_redirects=30,
                proxy=None,
                fname=None,
                fname_404=None,
                retry=3,
                timeout=10,
                is_get_real_url=False):
    """
    请求
    :param url:
    :param max_redirects:
    :param proxy:
    :param fname:
    :param fname_404:
    :param retry:
    :param timeout:
    :return:
    """

    ret = False
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 " \
                            "(KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"

    s = requests.session()
    s.max_redirects = max_redirects

    s.proxies = proxy

    while retry > 0:
        try:

            r = s.request(url=url,
                          method="GET",
                          headers=headers,
                          timeout=timeout,

                          )

            if r.reason == "OK":

                if fname:
                    if r.url != url:

                        # exists redirect
                        if is_get_real_url:
                            content = "<html><head><title>%s</title></head>" \
                                      "<body>%s</body></html>" % (r.url, url)
                        else:
                            content = r.content


                    else:
                        content = r.content

                    with codecs.open(fname, mode='wb') as fw:
                        fw.write(content)
                    ret = True
                else:
                    ret = r

                retry = 0

            elif r.reason == "Not Found":
                if fname_404:
                    with codecs.open(fname_404, mode='ab') as fw:
                        fw.write("%s%s" % (url, os.linesep))
                retry = 0

            else:
                logging.info("[url]: retry:%d %s, %s" % (retry, url, r.reason))
                retry = retry - 1

        except Exception as e:
            e = str(e)
            print(e)
            if is_get_real_url:
                ret = parse_request_error_str(e)
                if ret:
                    content = "<html><head><title>%s</title></head>" \
                              "<body>%s</body></html>" % (ret, url)

                    with codecs.open(fname, mode='wb') as fw:
                        fw.write(content)
                    ret = True
                    retry = 0
            else:

                logging.info("[REQUEST]: retry:%d %s %s" % (retry, url, e))

                retry = retry - 1

    return ret


@timeout_wrapper(1, do_other_thing)
def get_title(url, proxy=None, retry=1, timeout=10):
    """

    :param url:
    :param proxy:
    :param retry:
    :param timeout:
    :return:
    """
    if not url:
        return
    if not url.startswith("http"):
        url_all = "http://%s" % url
    else:
        url_all = url

    ret = get_request(url_all, proxy=proxy, retry=retry, timeout=timeout)

    if not ret:
        if not url.startswith("http"):
            url_all = "https://%s" % url
            ret = get_request(url_all, proxy=proxy, retry=retry, timeout=timeout)

    if ret:
        try:
            soup = BeautifulSoup(ret.content, 'lxml')

        except Exception as e:
            logging.error("GET title of %s failed : %s" % (url, repr(e)))
            return
        title = soup.find('title')
        if title:
            title = title.get_text()
            return strip_n(title)


def get_twitter_info(url, title="", ts="", tag="",
                     proxy=None,
                     root_dir="data/twitter", isnew=False, retry=1, timeout=10):
    """
    twitter解析
    :param short_url:
    :return:
    """

    file_404 = path("data/twitter_404")
    urls_404 = set()
    if os.path.exists(file_404):

        with codecs.open(file_404, mode='rb') as fr:
            for line in fr:
                line = line.strip()
                if line:
                    urls_404.add(line)

    if urls_404 and url in urls_404:
        return

    root_dir = path(root_dir)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

    hl = hashlib.md5()
    hl.update(url.encode(encoding='utf-8'))

    fname = path(root_dir, "%s.html" % hl.hexdigest())

    if isnew or not os.path.exists(fname):
        get_request(url, proxy=proxy, fname=fname, fname_404=file_404, retry=retry, timeout=timeout)

    if os.path.exists(fname):
        with codecs.open(fname, mode='rb') as fr:
            try:
                soup = BeautifulSoup(fr, 'lxml')

            except Exception as e:
                logging.error("GET title of %s failed : %s" % (url, repr(e)))
                return

            profile_header = soup.find("p", class_=re.compile(r'ProfileHeaderCard-bio'))

            if profile_header:
                profile_header = strip_n(profile_header.get_text())
            if not profile_header:
                profile_header = "None"

            profile_header_loc = soup.find("span", class_=re.compile(r'ProfileHeaderCard-locationText'))
            if profile_header_loc:
                profile_header_loc = strip_n(profile_header_loc.get_text())
            if not profile_header_loc:
                profile_header_loc = "None"

            profile_header_url = soup.find("span", class_=re.compile(r'ProfileHeaderCard-urlText'))
            if profile_header_url:
                profile_header_url = profile_header_url.find('a')
                if profile_header_url:
                    profile_header_url = strip_n(profile_header_url.get('title'))
            if not profile_header_url:
                profile_header_url = "None"

            profile_header_join = soup.find("span", class_=re.compile(r'ProfileHeaderCard-joinDateText'))
            if profile_header_join:
                profile_header_join = strip_n(profile_header_join.get('title'))
            if not profile_header_join:
                profile_header_join = "None"

            twitter_account = soup.find("a", class_=re.compile(r'ProfileHeaderCard-screennameLink'))
            if twitter_account:
                twitter_account = strip_n(twitter_account.get("href"))

            if not twitter_account:
                return

            overview = {
                "twitter_account": twitter_account,
                "profile_header_url": profile_header_url,
                "profile_header": profile_header,
                "profile_header_loc": profile_header_loc,
                "profile_header_join": profile_header_join,
                "url": url,
                "title": strip_n(title),
                'ts': ts,
                'tag': tag
            }
            return overview


@timeout_wrapper(1, do_other_thing)
def get_redirect_url(url,
                     proxy=None,
                     root_dir="data/shorturl",
                     isnew=False,
                     retry=1,
                     timeout=10,
                     source="secwiki",
                     issql=True):
    """

    :param urls:
    :return:
    """

    file_404 = path("data/shorturl_404")
    urls_404 = set()
    if os.path.exists(file_404):

        with codecs.open(file_404, mode='rb') as fr:
            for line in fr:
                line = line.strip()
                if line:
                    urls_404.add(line)

    if urls_404 and url in urls_404:
        return

    root_dir = path(root_dir)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

    hl = hashlib.md5()
    hl.update(url.encode(encoding='utf-8'))

    fname = path(root_dir, "%s.html" % hl.hexdigest())

    if isnew or not os.path.exists(fname):
        get_request(url, proxy=proxy, retry=retry, timeout=timeout, fname=fname,
                    fname_404=file_404, is_get_real_url=True)

    if os.path.exists(fname):
        with codecs.open(fname, mode='rb') as fr:
            try:
                soup = BeautifulSoup(fr, 'lxml')

            except Exception as e:
                logging.error("GET title of %s failed : %s" % (url, repr(e)))
                return

            title = soup.find("title")
            if title:
                title = title.get_text()
                if title.startswith("http"):
                    # title is the real url
                    o, ext = parse_url(title)
                    domain = o.netloc
                    url_path = o.path
                    root_domain = ext.domain + "." + ext.suffix

                    sql = "update {source}_detail " \
                          "set url='{title}',root_domain='{root_domain}', domain='{domain}',path='{path}' " \
                          "where url='{url}'; ".format(
                        root_domain=root_domain,
                        domain=domain,
                        path=url_path,
                        url=url,
                        title=title,
                        source=source

                    )

                    if issql:

                        return sql
                    else:
                        return {"domain": domain, "url": title}


def d2sql(d, table="github", action="replace"):
    """
    change dict 2 sql
    :param d:
    :return:
    """
    if not d:
        return

    column_names = ",".join(d.keys())
    column_values = ",".join(["'%s'" % i for i in d.values()])

    sql = "{action} into `{table}`({column_names}) values({column_values});".format(
        action=action,
        table=table,
        column_names=column_names,
        column_values=column_values
    )
    return sql


def parse_domain_tag(st):
    """

    :param st:
    :return:
    """
    if not st:
        return
    pattern = re.compile("^(\S+)\s+")
    match = re.match(pattern, st)
    if match:
        domain = match.groups()
        return domain[0]


def parse_sec_today_url(st):
    """

    :param st:
    :return:
    """
    if not st:
        return

    pattern = re.compile("^(\S+)\D+(\d*)(.+ago)")
    match = re.match(pattern, st)
    if match:
        domain, delta, day_detail = match.groups()
        if not day_detail.find("day") != -1:
            delta = 0
        else:
            delta = 0 - int(delta)
        ts = get_special_date(delta=delta)

        return domain, ts


def parse_request_error_str(st):
    """

    :param st:
    :return:
    """

    pattern = re.compile(
        r"HTTPS?ConnectionPool\(host='([^\x22]+)', port=(\d+)\): Max retries exceeded with url: (/\S*) \(")
    match = re.match(pattern, st)
    if match:
        host, port, url = match.groups()
        port = str(port)
        if port == 443:
            ret = "https://%s%s" % (host, url)
        else:
            ret = "http://%s%s" % (host, url)
        return ret


def test_get_weixin_info():
    """

    :return:
    """
    url = "https://mp.weixin.qq.com/s?__biz=MzU2NTc2MjAyNg" \
          "==&mid=2247483758&idx=1&sn=1bd0006d16747389046058ea34c3b7b7&chksm=fcb783ebcbc00afd694b7a2ee10ad32aff0a534963878541ee17974ffee29c63342f4e617661&token=1823181969&lang=zh_CN#rd"
    url = "https://mp.weixin.qq.com/s/RCpAUpFEzbSewEnWpHrsqw"
    ret = get_weixin_info(url=url)
    print(json.dumps(ret, indent=4))


def test_get_github_info():
    """

    :return:
    """
    url = "https://github.com/tanjiti/sec_profile"
    url = "https://github.com/ashishb/android-security-awesome"
    ret = get_github_info(url, isnew=False)
    print(ret)


def test_get_twitter_info():
    """

    :return:
    """
    url = "https://twitter.com/i/web/status/1085465178840346624"
    ret = get_twitter_info(url)
    print(ret)


def test_get_title():
    """

    :return:
    """
    pass


def test_get_requst():
    """

    :return:
    """
    url = "https://sec.today/pulses/"
    ret = get_request(url=url)
    print(ret)


if __name__ == "__main__":
    """
    """
    test_get_github_info()
    #test_get_weixin_info()
    # test_get_requst()

    # test_get_twitter_info()
