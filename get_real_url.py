# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from mills import get_redirect_url
from mills import SQLiteOper


def get_real_url(so, renew=False, proxy=None, retry=3, timeout=10):
    """

    :param so:
    :return:
    """
    urls = {
        "secwiki": set(),
        "xuanwu": set()
    }
    if proxy is not None:
        sql = "select distinct url from xuanwu_detail where " \
              "root_domain ='t.co' " \
              "or root_domain='bit.ly' " \
              "or root_domain='goo.gl' " \
              "or root_domain='ow.ly' " \
              "or root_domain='bddy.me' " \
              "or root_domain='buff.ly'	" \
              "or root_domain='intel.ly'" \
              "or root_domain='symc.ly'  " \
              "or root_domain='ht.ly' "

        result = so.query(sql)
        for item in result:
            item = item[0]
            if item:
                urls['xuanwu'].add(item)
    sql = "select distinct url from secwiki_detail where root_domain = 'dwz.cn' "
    result = so.query(sql)
    for item in result:
        item = item[0]
        urls['secwiki'].add(item)

    for k, v in urls.items():
        for vv in v:
            sql = get_redirect_url(vv, proxy=proxy,
                                   root_dir="data/shorturl",
                                   isnew=renew, retry=retry,
                                   timeout=timeout,
                                   source=k)
            if sql:
                so.execute(sql)
                print k, vv, sql


if __name__ == "__main__":
    """
    """
    proxy = None

    so = SQLiteOper("data/scrap.db")
    # 获取短链接真实url
    get_real_url(so, renew=False, proxy=proxy)
