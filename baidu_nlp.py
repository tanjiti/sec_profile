# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import logging
import re
import json

from aip import AipNlp


class Baidu_NLP(object):
    """

    """

    def __init__(self, conf=None, pos_wl=None):
        if conf is None:
            from conf.conf import conf
            conf = conf.get('baidu_nlp_account')

        if conf is None:
            return

        self.pos_wl = pos_wl


        self.client = AipNlp(conf.get("app_id"),
                             conf.get("api_key"),
                             conf.get("secret_key"))




    def seq_query(self, q, is_custom=False):
        """
        词法分析接口
        :param q:
        :return:
        """

        sts = set()

        try:
            if is_custom:
                ret = self.client.lexerCustom(q)

                print json.dumps(ret,indent=4)
            else:
                ret = self.client.lexer(q)
        except Exception as e:
            logging.error("[nlp_error]: %s e(%s)" %(q,str(e)))
            return

        if ret:

            if "items" in ret:
                for item in ret.get("items"):
                    pos = item.get("pos")

                    if self.pos_wl and pos not in self.pos_wl:
                        continue

                    iitem = item.get("item")

                    if pos and iitem:



                        sts.add((pos,iitem))


        return sts


if __name__ == "__main__":
    """
    """
    q = "2018年暗网非法数据交易总结"
    #q = "百度是一家高科技公司"

    pos_wl = ['n', 'nr', 'nz', 'ns', 'nt', 'nw', 'an', 'vn']

    client = Baidu_NLP(pos_wl=pos_wl)


    ret = client.seq_query(q,is_custom=True)
    if ret:
        for k,v in ret:
            print k,v
