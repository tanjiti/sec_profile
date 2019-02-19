# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import logging
import codecs

import re

from mills import path
from mills import SQLiteOper
from mills import get_title


def update_domain(so, retry=3, timeout=10, proxy=None):
    """

    :param so:
    :param retry:
    :param timeout:
    :param proxy:
    :return:
    """
    for table in ["secwiki_detail","xuanwu_detail"]:

        sql = 'select distinct domain  ' \
              'from {table} ' \
              'where domain_name is null or domain_name="" order by domain '.format(table=table)


        result = so.query(sql)
        for item in result:

            k = item[0]

            if not k:
                continue
            title = get_title(k, proxy=proxy, retry=retry, timeout=timeout)



            if title:
                title = re.sub('\x22', '', title)
                title = re.sub('\x27', '', title)
                update_sql = "update {table} set domain_name='{title}' where domain='{domain}';".format(
                    table=table,
                    title=title,
                    domain=k
                )
                try:
                    so.execute(update_sql)
                    print update_sql
                except Exception as e:
                    logging.error("[update_sql]: %s str(%s)" % (update_sql, str(e)))

def get_domain_name(so, source="secwiki", topn=5000):
    """

    :param so:
    :param source:
    :param topn:
    :return:
    """
    sql = "select domain,domain_name,count(path) as c from %s_detail group by domain order by c desc" %source


    ret = so.query(sql)

    if ret:
        i = 0

        for r in ret:

            if i < topn:
                domain,domain_name,c = r
                print domain,domain_name,c
            else:
                break
            i = i + 1


if __name__ == "__main__":
    """
    """
    proxy = None
    so = SQLiteOper("data/scrap.db")

    update_domain(so, retry=1, timeout=10, proxy=proxy)
    #获得安全网站排序列表
    for source in ["secwiki", "xuanwu",'github']: #
       get_domain_name(so, source=source, topn=50)
