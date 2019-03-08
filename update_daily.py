# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from secwiki_today import scraw as secwiki_scraw
from xuanwu_today import scraw as xuanwu_scraw
from mills import SQLiteOper
import visual


def scraw():
    """

    :return:
    """
    proxy = None
    so = SQLiteOper("data/scrap.db")
    #secwiki_scraw(so, proxy=proxy, delta=2)

    xuanwu_scraw(so, proxy=proxy, delta=2)


if __name__ == "__main__":
    """
    """
    scraw()

    visual.draw_readme()
