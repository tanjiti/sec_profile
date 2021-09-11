# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import logging
import datetime
import time

from bs4 import BeautifulSoup

from mills import d2sql
from mills import get_request
from mills import get_special_date
from mills import get_weixin_info
from mills import SQLiteOper


def datetime2timestamp(dt, tformat="%Y%m%d %H:%M:%S"):
    """
    datatime 2 timestamp
    :param dt:
    :param tformat:
    :return:
    """
    dt_ob = datetime.datetime.strptime(dt, tformat)

    return int(time.mktime(dt_ob.timetuple()))


def timestamp2datetime(ts, tformat="%Y%m%d %H:%M:%S"):
    """
    timestamp 2 datetime
    :param ts:
    :param tformat:
    :return:
    """
    # ts = ts - time.timezone
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(tformat)
    return timestamp


def scraw(so, proxy=None, delta=3):
    """

    :param so:
    :param proxy:
    :return:
    """
    ts_list = [get_special_date(delta, format="%Y%m%d") for delta in range(0, 0 - delta, -1)]

    keyword_map_dict = {
        'author': 'nickname_english',
        'title': 'title',
        'link': 'url',
        'pubDate': 'ts'
    }

    url = "http://wechat.doonsec.com/rss.xml"
    r = get_request(url)
    if r:
        try:
            soup = BeautifulSoup(r.content, 'xml')
        except Exception as e:
            logging.error("GET %s  failed : %s" % (url, repr(e)))
            return
        if soup:
            rows = soup.find_all("item")

            if rows:
                for row in rows:
                    if row:
                        d = {}

                        for child in row.children:

                            if child.name in keyword_map_dict:
                                field_name = keyword_map_dict[child.name]
                                field_value = child.text
                                if field_name:
                                    if field_name == 'ts':
                                        tformat = '%a, %d %b %Y %H:%M:%S'
                                        ts = datetime2timestamp(field_value[0:-6], tformat=tformat)
                                        field_value = timestamp2datetime(ts, tformat="%Y%m%d")
                                        if field_value not in ts_list:
                                            continue

                                    d[field_name] = field_value

                        if d:
                            # 获得weixin_no
                            weixin_info = get_weixin_info(url=d.get('url'))

                            if weixin_info:
                                weixin_no = weixin_info.get('weixin_no')
                                d['weixin_no'] = weixin_no
                            sql = d2sql(d, table='weixin')

                            if sql:
                                try:
                                    print(sql)
                                    so.execute(sql)
                                except Exception as e:
                                    logging.error("[sql]: %s %s" % (sql, str(e)))


if __name__ == "__main__":
    """
    """
    proxy = None
    so = SQLiteOper("data/scrap.db")
    scraw(so, proxy=proxy, delta=7)
