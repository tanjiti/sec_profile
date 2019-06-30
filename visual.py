# -*- coding: utf-8 -*-
import os
import re
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from collections import OrderedDict
import matplotlib.pyplot as plt


import matplotlib
print(matplotlib.matplotlib_fname())

from mills import SQLiteOper
from mills import path
from mills import get_special_date


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

    if table == "secwiki_detail" and int(year) >= 2019:
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


def statistict_github_language(so, topn=132, reverse=True, year=''):
    """

    :param so:
    :return:
    """

    lang_dict = {}
    sql = "select distinct repo_lang from github where ts like '{year}%' and (repo_lang is not null or repo_lang != '')".format(
        year=year)
    # print sql
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
    fname = path("data", "%s_github_lang.txt" % year)
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
        ods = statistict_github_language(so, topn=top, year=year)

    labels = []
    values = []
    if not ods:
        return
    for k, v in ods.items():
        labels.append(k)
        values.append(v)

    labels.append("other")
    values.append(1 - sum(values))

    explode = [0.1 for _ in range(0, len(labels))]
    explode[-1] = 0  # 凸显

    try:
        #plt.rcParams['font.sans-serif'] = ['MicrosoftYaHei']
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
        plt.rcParams['font.family'] = 'sans-serif'
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

            title_pie = "%s-最喜欢语言占比" % (year)

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
    except Exception as e:
        print source, year, tag
        print len(labels), labels
        print len(values), values
        print len(explode), explode


def main_pie(year):
    """

    :return:
    """
    so = SQLiteOper("data/scrap.db")

    for tag in ["domain", "tag"]:
        for source in ["secwiki", "xuanwu"]:
            draw_pie(so, source=source, year=str(year), tag=tag, top=10)

    draw_pie(so, tag="language", top=25, year=year)


def draw_table(so, source="weixin", top=100, year="2019"):
    """

    :param so:
    :param source:
    :param top:
    :return:
    """
    if source == "weixin":
        sql = "select nickname_english,weixin_no,url,title,count(*) as c from weixin where ts like '{year}%' and nickname_english != '' group by nickname_english order by ts desc limit {top} "
        header = ["nickname_english", "weixin_no", "url", "title"]

    elif source == "github_org":
        sql = "select github_id,title,url,org_url,org_profile,org_geo," \
              "org_repositories,org_people,org_projects," \
              "repo_lang,repo_star,repo_forks," \
              "count(*) as c from github  where github_type=1 and ts like '{year}%' group by github_id order by repo_forks desc,org_repositories desc,org_projects desc limit {top} "
        header = ["github_id", "title", "url", "org_url", "org_profile", "org_geo", "org_repositories",
                  "org_people", "org_projects", "repo_lang", "repo_star", "repo_forks"]

    elif source == "github_private":
        sql = "select github_id,title,url,p_url,p_profile,p_loc,p_company," \
              "p_repositories,p_projects," \
              "p_stars,p_followers,p_following," \
              "repo_lang,repo_star,repo_forks ," \
              "count(*) as c from github  where github_type=0 and ts like '{year}%' group by github_id order by p_followers desc limit {top}"
        header = ["github_id", "title", "url", "p_url", "p_profile", "p_loc", "p_company", "p_repositories",
                  "p_projects", "p_stars", "p_followers", "p_following", "repo_lang", "repo_star", "repo_forks "]
    else:
        return

    try:
        ret = so.query(sql.format(top=top, year=year))
    except Exception as e:
        print sql, str(e)
        return

    rets = []
    rets.append(header)

    for r in ret:
        rets.append(list(r))
    return rets


def markdown_table(rets):
    """

    :param rets:
    :return:
    """
    markdown_rets = []
    if not rets:
        return

    header = rets[0]
    header_str = " | ".join(header)
    header_str = "| %s| " % header_str
    header_sep = ["---" for _ in rets[0]]
    header_sep_str = " | ".join(header_sep)
    header_sep_str = "| %s| " % header_sep_str

    markdown_rets.append(header_str)
    markdown_rets.append(header_sep_str)

    for ret in rets[1:]:
        column_str = " | ".join([str(_) for _ in ret])
        column_str = "| %s| " % column_str
        markdown_rets.append(column_str)

    return markdown_rets


def draw_readme(fpath=None):
    """

    :return:
    """

    if fpath is None:
        fpath = "README.md"

    tables_rets = []
    so = SQLiteOper("data/scrap.db")
    year = get_special_date(delta=0, format="%Y%m")


    # update

    main_pie(year)

    # update weixin,github
    sources = ["weixin", "github_org", "github_private"]

    d = {
        "weixin": "微信公众号",
        "github_org": "组织github账号",
        "github_private": "私人github账号"
    }

    for source in sources:
        rets = draw_table(so, top=100, source=source, year=year)
        if rets:

            markdown_rets = markdown_table(rets)
            if markdown_rets:
                tables_rets.append("# %s 推荐" % d.get(source, source))
                for markdown_ret in markdown_rets:
                    tables_rets.append(markdown_ret)
                tables_rets.append(os.linesep)

    with codecs.open(fpath, mode='wb') as fr:
        fr.write("# [数据年报](README_YEAR.md)")
        fr.write(os.linesep)
        fr.write("# [数据月报-6月](README_6.md)")
        fr.write(os.linesep)
        fr.write("# [数据月报-5月](README_5.md)")
        fr.write(os.linesep)
        fr.write("# [数据月报-4月](README_4.md)")
        fr.write(os.linesep)
        fr.write("# [数据月报-3月](README_3.md)")
        fr.write(os.linesep)
        fr.write('# %s 信息源与信息类型占比' % year)
        fr.write(os.linesep)
        fr.write('![{year}-信息源占比-secwiki](data/img/domain/{year}-信息源占比-secwiki.png)'.
                 format(year=year))
        fr.write(os.linesep)
        fr.write(os.linesep)
        fr.write('![{year}-信息源占比-xuanwu](data/img/domain/{year}-信息源占比-xuanwu.png)'.
                 format(year=year))
        fr.write(os.linesep)
        fr.write(os.linesep)
        fr.write('![{year}-信息类型占比-secwiki](data/img/tag/{year}-信息类型占比-secwiki.png)'.
                 format(year=year))
        fr.write(os.linesep)
        fr.write(os.linesep)
        fr.write('![{year}-信息类型占比-xuanwu](data/img/tag/{year}-信息类型占比-xuanwu.png)'.
                 format(year=year))
        fr.write(os.linesep)
        fr.write(os.linesep)

        fr.write('![{year}-最喜欢语言占比](data/img/language/{year}-最喜欢语言占比.png)'.format(year=year))
        fr.write(os.linesep)
        fr.write(os.linesep)

        st = os.linesep.join(tables_rets)
        fr.write(st)
        fr.write(os.linesep)
        fr.write(os.linesep)

        fr.write('# 日更新程序')
        fr.write(os.linesep)
        fr.write('`python update_daily.py`')


if __name__ == "__main__":
    """
    """
    fpath = "README.md"
    draw_readme()
