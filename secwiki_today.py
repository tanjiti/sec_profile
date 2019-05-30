# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import logging
import re

from bs4 import BeautifulSoup

from mills import get_request
from mills import get_special_date
from mills import strip_n
from mills import parse_url

from mills import d2sql
from mills import get_title

from mills import SQLiteOper
from mills import get_github_info
from mills import get_weixin_info
from mills import get_twitter_info


def scraw(so, proxy=None, delta=3):
    """

    :param so:
    :param proxy:
    :return:
    """
    ts_list = [get_special_date(delta, format="%Y-%m-%d") for delta in range(0, 0 - delta, -1)]

    url = "https://www.sec-wiki.com/?2019-03-04"
    r = get_request(url)
    if r:
        try:
            soup = BeautifulSoup(r.content, 'lxml')


        except Exception as e:
            logging.error("GET %s  failed : %s" % (url, repr(e)))
            return
        if soup:
            rows = soup.find_all("span", class_='dropcap')

            if rows:

                for row in rows:

                    if row:


                        cur_ts = row.get_text()
                        if cur_ts in ts_list:
                            a = row.next_sibling

                            if a:
                                url = a.get("href")

                                o, ext = parse_url(url)
                                domain = o.netloc
                                cur_ts = re.sub("-", "", cur_ts)

                                title = strip_n(a.get_text())
                                overview = {}
                                overview['ts'] = cur_ts
                                overview['url'] = url
                                overview['title'] = title
                                overview['domain'] = domain
                                overview["domain_name"] = \
                                    str(get_title(overview["domain"], proxy=proxy))

                                if overview:
                                    sql = d2sql(overview, table="secwiki_today_detail",
                                                action="INSERT OR IGNORE ")

                                    if sql:
                                        try:
                                            so.execute(sql)
                                        except Exception as e:
                                            logging.error("[secwiki_today_sql]: "
                                                          "sql(%s) error(%s)" % (sql, str(e)))

                                    st = "{ts}\t{url}" \
                                         "\t{title}\t{domain}\t{domain_name}".format(
                                        ts=overview.get("ts"),
                                        domain=overview.get("domain"),
                                        title=overview.get("title"),
                                        domain_name=overview.get("domain_name"),
                                        url=overview.get("url")
                                    )
                                    print st

                                    url = overview.get("url")
                                    ts = overview.get("ts")
                                    tag = overview.get("tag", "")
                                    title = overview.get("title")

                                    sql = ""

                                    if url.find("://twitter.com") != -1:

                                        d = get_twitter_info(url, title, ts=ts, tag=tag, proxy=proxy)

                                        if d:
                                            sql = d2sql(d, table="twitter")

                                    elif url.find("weixin.qq.com") != -1:
                                        d = get_weixin_info(url, ts, tag)

                                        if d:
                                            sql = d2sql(d, table="weixin")
                                    elif url.find("//github.com") != -1:
                                        d = get_github_info(url, title, ts=ts, tag=tag)

                                        if d:
                                            sql = d2sql(d, table='github')

                                    if sql:
                                        try:
                                            print sql
                                            so.execute(sql)
                                        except Exception as e:
                                            logging.error("[sql]: %s %s" % (sql, str(e)))


if __name__ == "__main__":
    """
    """
    proxy = None
    so = SQLiteOper("data/scrap.db")
    scraw(so, proxy=proxy)
