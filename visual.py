# -*- coding: utf-8 -*-
import os
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from collections import OrderedDict
import matplotlib.pyplot as plt

from mills import SQLiteOper
from mills import path


def info_source(so, table="secwiki_detail", year="", top=100, tag="domain"):
    """
    按tag或domain分组
    :param so:  sqlite3db
    :param table:
    :param year:
    :param top:
    :param tag: domain 或者 tag
    :return:
    """
    if table == "xuanwu_detail" and int(year) >= 2019:
        table = "xuanwu_today_detail"

    if table == "secwiki_detail" and int(year) >= 2019 and tag=="domain":
        table = "secwiki_today_detail"

    od = OrderedDict()
    sql = 'select {tag},count(url) as c ' \
          'from {table} ' \
          'where ts like "%{year}%" ' \
          'group by {tag} ' \
          'order by c desc '.format(table=table, year=year, tag=tag)



    result = so.query(sql)
    for item in result:
        od[item[0]] = item[1]

    od_perct = OrderedDict()
    sum_count = sum(od.values())

    i = 0
    for k, v in od.items():
        """
        """
        if i < top:
            od_perct[k] = round(float(v) / sum_count, 4)
        else:
            break
        i = i + 1

    return od_perct


def statistict_github_language(so, topn=132, reverse=True):
    """

    :param so:
    :return:
    """
    lang_dict = {}
    sql = "select distinct repo_lang from github where repo_lang is not null or repo_lang != ''"
    result = so.query(sql)
    if result:
        for item in result:
            repo_lang = item[0]
            repo_langs = [_.strip() for _ in re.split(',', repo_lang)]
            for repo_lang in repo_langs:
                if not repo_lang:
                    continue
                if repo_lang in lang_dict:
                    lang_dict[repo_lang] = lang_dict[repo_lang] + 1
                else:
                    lang_dict[repo_lang] = 1

    vd = OrderedDict(sorted(lang_dict.items(), key=lambda t: t[1], reverse=reverse))
    sum_count = sum(vd.values())
    vd2 = OrderedDict()

    i = 0
    for k, v in vd.items():
        if i < topn:
            vd2[k] = round(float(v) / sum_count, 4)
        else:
            break
        i = i + 1
    fname = path("data", "github_lang.txt")
    with open(fname, mode='wb') as fw:
        for k, v in vd.items():
            fw.write("%s\t%s%s" % (k, v, os.linesep))

    return vd2


def draw_pie(so, source="secwiki", year="", tag="domain", top=10):
    """

    :return:
    """
    if tag != "language":

        ods = info_source(so, table="{source}_detail".format(source=source),
                          top=top,
                          year=str(year),
                          tag=tag)
    else:
        ods = statistict_github_language(so, topn=top)


    labels = []
    values = []
    if not ods:
        return
    for k, v in ods.items():
        labels.append(k)
        values.append(v)

    labels.append("other")
    values.append(1 - sum(values))

    explode = [0.1 for _ in range(0, top + 1)]
    explode[-1] = 0  # 凸显

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
    plt.rcParams['axes.unicode_minus'] = False  # 坐标轴负号的处理
    plt.axes(aspect='equal')  # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.pie(values,  # 指定绘图的数据
            explode=explode,  # 指定饼图某些部分的突出显示，即呈现爆炸式
            labels=labels,  # 为饼图添加标签说明，类似于图例说明
            labeldistance=1.2,  # 设置各扇形标签（图例）与圆心的距离；
            pctdistance=0.6,  # ：设置百分比标签与圆心的距离；
            startangle=90,  # 设置饼图的初始摆放角度；
            shadow=True,  # 是否添加饼图的阴影效果；
            autopct='%3.2f%%')

    if tag == "domain":
        title_pie = "%s-信息源占比-%s" % (year, source)
    elif tag == "tag":
        title_pie = "%s-信息类型占比-%s" % (year, source)
    elif tag == "language":

        title_pie = "最喜欢语言占比"

    else:
        return

    plt.title(unicode(title_pie))

    fdir = path("data/img/%s" % tag)
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    fpath = path(fdir, "%s.png" % title_pie)

    plt.legend(labels, loc='upper right', fontsize=5)

    plt.savefig(fpath)

    plt.close()


def main_pie():
    """

    :return:
    """
    so = SQLiteOper("data/scrap.db")

    for tag in ["domain", "tag"]:
        for source in ["secwiki", "xuanwu"]:
            for year in [2014, 2015, 2016, 2017, 2018, 2019]:
                draw_pie(so, source=source, year=str(year), tag=tag, top=10)

    draw_pie(so, tag="language", top=25)

def draw_table(so,source="secwiki",top=10):
    """

    :param so:
    :param source:
    :param top:
    :return:
    """

def main_table():
    """

    :return:
    """
    so = SQLiteOper("data/scrap.db")
    for source in ["secwiki","xuanwu"]:
        draw_table(so,source=source,top=10)

if __name__ == "__main__":
    """
    """
    main_pie()

