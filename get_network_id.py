# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import re
import logging

from mills import SQLiteOper
from mills import get_weixin_info
from mills import get_github_info
from mills import get_twitter_info
from mills import d2sql


def get_network_id(so, source="weixin", proxy=None, retry=3, timeout=10):
    """

    :param so:
    :param source:
    :param renew:
    :return:
    """

    if source == "weixin":
        keyword = "://mp.weixin.qq.com/"
    elif source == "github":
        keyword = "https://github.com/"
    elif source == "twitter":
        keyword = "//twitter.com"
    elif source == "zhihu":
        keyword = "://zhuanlan.zhihu.com"
    elif source == "weibo":
        keyword = "://weibo.com"
    elif source == "medium":
        keyword = "medium.com"
    else:
        return

    # get urls

    for info_source in ["secwiki", "xuanwu"]:

        sql = "select " \
              "distinct url,title,ts,tag " \
              "from {source}_detail where url like '%{keyword}%'".format(
            keyword=keyword,
            source=info_source
        )

        result = so.query(sql)
        for item in result:
            url = item[0]
            title = item[1]
            ts = item[2]
            tag = item[3]

            pos = url.find('http', 2)
            if pos != -1:
                url = item[0:pos]

            if not url:
                continue
            try:
                url = re.sub('\x22', '', url)
                url = re.sub('\x27', '', url)
            except Exception as e:
                logging.error("[URL_ERROR]: url(%s) e(%s)" % (url, str(e)))
                continue
            try:
                title = re.sub('\x22', '', title)
                title = re.sub('\x27', '', title)
            except Exception as e:
                logging.error("[title_ERROR]: title(%s) e(%s)" % (url, str(e)))
                continue

            update_sql = ""
            if source == "weixin":
                details = get_weixin_info(url, ts=ts, tag=tag)
                if details:
                    update_sql = d2sql(details, table='weixin', action='replace')


            elif source == "github":

                details = get_github_info(url, title, ts=ts, tag=tag)
                if details:
                    update_sql = d2sql(details, table='github', action='replace')


            elif source == "twitter":

                details = get_twitter_info(url, title, ts=ts, tag=tag,
                                           proxy=proxy,
                                           retry=retry, timeout=timeout)

                if details:
                    update_sql = d2sql(details, table='twitter', action='replace')




            else:

                print url
                print title

            if update_sql:
                try:
                    print update_sql
                    so.execute(update_sql)
                except Exception as e:
                    logging.error("[replace_failed]: %s e(%s)" % (update_sql, str(e)))


if __name__ == "__main__":
    """
    """
    proxy = {
        # "socks:": "socks://127.0.0.1:1080",
        "http": "http://127.0.0.1:1081",
        'https': "http://127.0.0.1:1081"

    }
    #proxy = None
    so = SQLiteOper("data/scrap.db")

    # 获得安全从业人员账号
    for source in ['github']:  # 'github',  'twitter']:
        get_network_id(so, source=source)
