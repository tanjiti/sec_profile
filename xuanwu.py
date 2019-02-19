# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import os
import glob
import re
import codecs
import logging
import unicodedata
import datetime

import requests
from bs4 import BeautifulSoup

from mills import get_special_date
from mills import path
from mills import parse_url
from mills import SQLiteOper
from mills import get_weixin_info
from mills import get_github_info
from mills import get_twitter_info
from mills import d2sql
from mills import strip_n


def parse_body(t, day):
    """
    [ Others ]  在非浏览器软件中验证 SSL 证书：   https://pdfs.semanticscholar.org/48fc/8f1aa0b6d1e4266b8017820ff8770fb67b6f.pdf

    :param t:
    :return:
    """
    result = None

    p = t.text

    p = p.replace("\n", "")
    p = unicodedata.normalize("NFKC", p)

    # 查找urls
    url_pattern = r"https?:\/{2}\S+"
    pattern = re.compile(url_pattern)

    m = re.findall(pattern, p)

    if m:
        urls = m

        # 查找tag与文章标题
        all_pattern = r'^\[\W*(\w*).*\]\s*(.+)http'
        pattern = re.compile(all_pattern)
        m = re.search(pattern, p)
        if m:

            tag = m.group(1)
            title = m.group(2)


        else:
            logging.error("[BAD_REGEX_TAG]: %s %s" % (day, p))
            tag = "Others"
            title = ""
        result = [tag, urls, title]


    else:
        # logging.error("[BAD_REGEX_URL]: day(%s) text(%s)" % (day, p))
        result = None

    return result


def parse_author(au, day):
    """
    查找twiiter id
    :param au:
    :return:
    """
    p = re.compile(r'(@\w+)')
    m = re.search(p, au)
    if m:

        twitter_id = m.group(1)
    else:

        twitter_id = ""
        logging.error("[BAD_AUTHOR]: %s %s" % (day, au))

    return twitter_id


def scrap_item(cur_day=None):
    """

    :return:
    """
    year = cur_day[0:4]
    month = cur_day[4:6]
    day = cur_day[6:8]

    fname = path("data/xuanwu/{year}/{month}/{day}/index.html".format(year=year, month=month, day=day))

    url = """https://xuanwulab.github.io/cn/secnews/{year}/{month}/{day}/index.html""".format(year=year, month=month,
                                                                                              day=day)
    print url
    logging.info("[SCRAP_PAGE]: %s" % url)
    try:

        r = requests.get(url)
        if r.status_code == 200:
            fname_year = path("data/xuanwu/{year}".format(year=year))

            if not os.path.exists(fname_year):
                os.mkdir(fname_year)
            fname_month = path("data/xuanwu/{year}/{month}".format(year=year, month=month))

            if not os.path.exists(fname_month):
                os.mkdir(fname_month)

            fname_day = path("data/xuanwu/{year}/{month}/{day}".format(year=year, month=month, day=day))

            if not os.path.exists(fname_day):
                os.mkdir(fname_day)

            with codecs.open(fname, mode='wb') as fw:
                fw.write(r.content)

                return fname

    except Exception as e:
        logging.error("[SCRAP_REQUEST_FAILED]: %s %s" % (url, str(e)))


def getdatefrompath(fname):
    """

    :return:
    """
    p = re.compile(r'(\d{4})\/(\d{2})\/(\d{2})\/index\.html')

    m = re.search(p, fname)
    if m:
        cur_day = m.group(1) + m.group(2) + m.group(3)
        return cur_day


def getstartendfrompath(fnames):
    """

    :param fnames:
    :return:
    """

    start = 0
    end = 0
    for fname in fnames:
        cur_day = getdatefrompath(fname)

        if cur_day:
            cur_day = int(cur_day)
            if start == 0:
                start = cur_day
                end = cur_day
            else:
                if cur_day < start:
                    start = cur_day
                else:
                    end = cur_day
    return start, end


def getmissdate():
    """
    获取缺失的日期
    :return:
    """

    days = []
    cur_fname_lists = []

    for fname in glob.glob(r'data/xuanwu/*/*/*/index.html'):
        cur_fname_lists.append(fname)
    start, end = getstartendfrompath(cur_fname_lists)

    cur_day = get_special_date()
    print "cur_day({cur_day}), last_day({last_day})".format(cur_day=cur_day, last_day=end)
    if end != 0:
        last_day = datetime.datetime.strptime(str(end), '%Y%m%d')
        cur_day = datetime.datetime.strptime(str(cur_day), '%Y%m%d')
        delta = cur_day - last_day
        for i in range(1, delta.days + 1):
            n_day = last_day + datetime.timedelta(days=i)
            n_day = n_day.strftime('%Y%m%d')
            days.append(n_day)
    return days


def parse_item(fname, so=None, proxy=None):
    """
    解析单个页面
    :param page:
    :return:
    """

    cur_day = getdatefrompath(fname)

    if cur_day is None:
        return

    if os.path.exists(fname):
        html_hd = open(fname, mode='rb')

        soup = BeautifulSoup(html_hd, "lxml")

        divs = soup.find_all(id='singleweibo')
        for div in divs:

            if div:

                weibo_id = ""

                weibo_author = div.find(id="singleweiboauthor")
                if weibo_author:
                    if weibo_author.p:
                        try:
                            weibo_id = parse_author(weibo_author.p.text, cur_day)
                        except Exception as e:

                            logging.error("[PARSE_AUTHOR_FAILED]: %s %s %s" % (cur_day, str(e), weibo_author.p))

                weibo_body = div.find(id="singleweibobody")
                if weibo_body:
                    try:
                        r = parse_body(weibo_body.p, cur_day)
                        if r:
                            tag = r[0]
                            urls = r[1]
                            title = r[2]
                            if urls:
                                for url in urls:
                                    o, ext = parse_url(url)
                                    domain = o.netloc
                                    url_path = o.path
                                    root_domain = ext.domain + "." + ext.suffix

                                    result = (cur_day, tag, url, title,
                                              root_domain, domain, url_path, weibo_id)

                                    title = strip_n(title)
                                    sql = ""

                                    if url.find("://twitter.com") != -1:

                                        d = get_twitter_info(url, title, ts=cur_day, tag=tag, proxy=proxy)

                                        if d:
                                            sql = d2sql(d, table="twitter")

                                    elif url.find("//weixin.qq.com") != -1:
                                        d = get_weixin_info(url, cur_day, tag)

                                        if d:
                                            sql = d2sql(d, table="weixin")
                                    elif url.find("//github.com") != -1:
                                        d = get_github_info(url, title, ts=cur_day, tag=tag)

                                        if d:
                                            sql = d2sql(d, table='github')
                                    if sql:
                                        try:
                                            so.execute(sql)
                                        except Exception as e:
                                            logging.error("[sql]: %s %s" % (sql, str(e)))

                                    yield result
                    except Exception as e:

                        logging.error("[PARSE_BODY_FAILED]: %s %s %s" % (cur_day, str(e), weibo_body.p))

        html_hd.close()


def parse_all(renew=False, ndays=None, proxy=None):
    """
    解析多个页面
    :return:
    """
    so = SQLiteOper("data/scrap.db")

    # 解析或爬取缺失的页面
    fname_lists = []
    if ndays is not None:

        for cur_day in ndays:
            year = cur_day[0:4]
            month = cur_day[4:6]
            day = cur_day[6:8]
            fname = path("data/xuanwu/{year}/{month}/{day}/index.html".format(year=year, month=month, day=day))

            if not os.path.exists(fname):

                fname = scrap_item(cur_day)
                if fname is None:
                    print "%s news not exits" % cur_day

                else:
                    fname_lists.append(fname)

    if renew:
        fname_lists = []
        # 重新解析所有页面
        sql = 'delete from `xuanwu_detail`'
        so.execute(sql)
        for fname in glob.iglob(r'data/xuanwu/*/*/*/index.html'):
            fname_lists.append(fname)

    if fname_lists:
        start, end = getstartendfrompath(fname_lists)
        sql = """
                    insert into `xuanwu_detail`(`ts`,`tag`,`url`,`title`,`root_domain`,`domain`,`path`,`author_id`)
                        values(?,?,?,?,?,?,?,?);
                    """
        # file handler
        result_fname = path("data/xuanwu_{start}_{end}.txt".format(
            start=start,
            end=end
        ))

        if not renew and os.path.isfile(result_fname) and os.path.getsize(result_fname) > 0:
            return

        result_fh = codecs.open(result_fname, mode='wb')

        for fname in fname_lists:

            fname = path(fname)

            results_list = {}
            for content in parse_item(fname, so=so, proxy=proxy):
                if content:
                    k = content[0] + content[2]

                    results_list[k] = content
                    line = "\t".join(content)
                    print line
                    result_fh.write("{line}{linesep}".format(line=line, linesep=os.linesep))

            if results_list:
                so.executemany(sql, operate_list=results_list.values())


def main(renew=False):
    """

    :param renew:  全量更新或增量更新
    :return:
    """
    ndays = getmissdate()
    parse_all(ndays=ndays, renew=renew, proxy=None)


if __name__ == "__main__":
    """
   
    """
    main(renew=False)
