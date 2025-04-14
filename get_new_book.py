import os
import re
import time
import logging

import mills
from mills import get_request, timestamp2datetime
from mills import SQLiteOper
from mills import d2sql
from mills import strip_n
import xml.etree.ElementTree as ET
import lxml
import codecs
import requests

from bs4 import BeautifulSoup

def get_bookname_from_url(url=None):
    """

    <![CDATA[ Beginner's Guide to Streamlit with Python ]]>
    https://it-ebooks.info/book/1686051862-beginners_guide_to_streamlit_with_python
    """
    s = 'https://it-ebooks.info/book/'

    if not url:
        return
    url = url.strip()
    p = r'^\d+\-([^\/]+)\/'
    if url.startswith(s):
        parts = url.split(s)
        bookname = parts[-1]
        if '_' in bookname:
            m = re.search(p, bookname)
            if m:
                bookname = m.groups()[0]
                bookname = bookname.replace("_", " ")
                return bookname


class GetNewBook(object):
    """
    get new book
    """

    def __init__(self, **kwargs):
        """
        init
        :param kwargs:
        """
        self.rss_url_dict = {
            'libgen': [
                'https://libgen.is/rss/index.php'
                #'https://libgen.rs/rss/index.php',
                #'https://libgen.st/rss/index.php',
                #'https://libgen.li/rss/index.php'

             ],
            'wow': 'https://feeds.feedburner.com/wowebook',
            #'it-ebooks': 'https://it-ebooks.info/rss.xml',
            #'libgen': 'https://libgen.onl/feed/',


        }
        self.json_url_dict = {
            'libgen': '/json.php?object=f&mode=last&timefirst=2024-08-25&timelast=2024-08-26'
        }

        self.cybersecurity_keyword = [
            # common
            ['python'],
            ['rust'],
            ['kubernetes'],
            ['cybersecurity'],
            # application/api/network/cloud/windows/linux/endpoint/mobile
            # ['secure'],
            ['endpoint', 'detection'],
            ['playbook'],
            ['defensive', 'security'],
            ['offensive', 'security'],
            ['prompt', 'engineer'],
            ['large', 'language'],
            ['ai', 'agents'],
            ['monitor'],
            ['secure', 'coding'],
            ['monitoring'],
            ['reconnaissance'],
            ['network', 'traffic'],
            ['defense', 'strategies'],
            ['password', 'cracking'],
            ['dark', 'web'],
            ['kali'],
            ['detect'],
            ['attack'],
            ['hacker'],
            ['hacking'],
            ['securing'],
            ['asset'],
            ['forensics'],
            ['risk', 'management'],
            ['malware'],
            ['botnet'],
            ['ransomware'],
            ['ddos'],
            ['beacon'],
            ['observability'],
            # ['assessment'],
            ['vulnerability'],
            ['honeypot'],
            ['deceptions'],
            ['iast'],  # interactive application security testing
            ['sast'],  # static application security
            ['dast'],  # dynamic application security
            ['security', 'testing'],
            ['security', 'detection'],
            ['penetration'],
            ['supply', 'chain'],
            ['threat', 'modeling'],
            ['threat', 'detection'],
            ['aws', 'security'],
            ['opentelemetry'],
            ['telemetry'],
            # threat intelligence
            ['threat', 'intelligence'],
            ['threat', 'hunting'],
            ['cyber', 'intelligence'],
            ['hunter'],
            ['att&ck'],
            ['reverse', 'engineering'],
            ['bug', 'bounty'],
            ['crypto'],
            ['cryptography'],
            ['fraud'],
            # auto
            ['attack', 'vectors'],
            ['social', 'engineering'],
            ['attack', 'simulation'],

            # productor
            ['cloud', 'security'],
            ['information', 'security'],
            ['security', 'information' 'event', 'management'],
            ['siem'],
            ['security', 'orchestration', 'automation', 'response'],
            ['soar'],
            ['security', 'operation', 'center'],
            ['security', 'operations'],

            ['detection', 'response'],  # xDR
            ['deep', 'packet', 'inspection'],
            ['firewall'],
            ['intrusion'],
            ['incident', 'response'],
            ['incident', 'management'],
            ['zero', 'trust'],
            ['access', 'management'],
            ['iam'],  # identity and access management
            ['privileged'],
            ['hardening'],
            ['assurance'],
            ['mfa'],
            ['authentication'],
            ['devsec'],
            ['bule', 'team'],
            ['fuzzing'],
            ['evading'],
            ['red', 'team'],
            ['purple', 'team'],
            ['blue', 'team'],
            ['attack', 'simulation'],
            ['black', 'hat'],
            ['white', 'hat'],
            ['privacy'],
            ['compliance'],
            ['debug'],
            ['debugging'],
            ['exploit'],
            ['exploitation'],
            ['binary'],
            ['rootkits'],
            ['osint'],

            ['falcon'],
            ['sentinel'],  # microsoft
            ['defender'],  # microsoft
            ['defense'],
            ['copilot'], # microsoft
            ['palo', 'alto'],
            ['qrader'],  # ibm
            ['falcon'],
            ['cobaltstrike'],
            ['microsoft'],
            ['cuckoo'],
            ['mitre'],
            ['sans'],
            ['ebpf'],
            ['fortinet'],
            ['ansible'],
            ['spring', 'security'],

            ['comptia'],
            ['selinux'],
            ['pentesting'],
            ['devops'],
            ['devsecops'],
            ['network', 'analysis'],
            ['wireshark'],
            ['soc', 'analyst'],
            ['api', 'security'],
            ['elastic', 'stack'],
            # AI
            ['generative'],
            ['ai', 'agent'],
            ['chatgpt'],
            ['langchain'],
            ['copilot'],
            ['openai'],
            ['prompt', 'engineering'],
            # abnormal check
            ['time','series'],
            ['splunk'],
            ['snort'],
            ['firewalls'],

        ]
        self.book_language_list = ['English']

    def _is_hit_keyword(self, title=None, keyword_list=None):
        """

        :param title:
        :param keyword:
        :return:
        """
        is_hit = False
        if not keyword_list:
            return is_hit
        if not title:
            return is_hit

        title = title.lower()
        title_parts = re.split('\s+', title)
        title_parts = [_.replace(':', '') for _ in title_parts]
        title_parts = [_.replace(',', '') for _ in title_parts]

        num_of_keyword = len(keyword_list)

        if num_of_keyword == 1:
            if keyword_list[0].lower() in title_parts:
                is_hit = True
                return is_hit
        else:
            num_of_hit = 0
            for kw in keyword_list:
                if kw.lower() in title_parts:
                    num_of_hit += 1

            if num_of_hit == num_of_keyword:
                is_hit = True
                return is_hit

        return is_hit

    def is_security_book(self, title):
        """
    check security book
        :param title:
        :return:
        """
        is_hit = False
        # split title

        for kw in self.cybersecurity_keyword:
            if not isinstance(kw, list):
                kw_list = [kw]
            else:
                kw_list = kw
            is_hit = self._is_hit_keyword(title=title, keyword_list=kw_list)

            if is_hit:
                return is_hit

        return is_hit

    def parse_xml(self, fname=None):
        """
        parse lxml
        :param fname:
        :return:
        """
        if not os.path.exists(fname):
            return

        with codecs.open(fname, mode='rb') as fr:
            c = fr.read()
            c = c.strip()
            soup = BeautifulSoup(c, 'lxml')
            articles = soup.findAll('item')
            sql_list = []

            for a in articles:
                book_dict = {}
                title = a.find('title').text.encode('utf-8')
                link = a.link.next_sibling.encode('utf-8')
                description = a.find('description')
                pubdate = a.find('pubdate')
                if not title and link:
                    title = get_bookname_from_url(link)

                if pubdate:
                    pubdate = pubdate.text
                    if pubdate:
                        try:
                            # Sun, 22 Oct 2023 09:09:52 +0000
                            parts = re.split(r' ', pubdate)
                            pubdate = " ".join(parts[0:-1])
                            date_format = "%a, %d %b %Y %H:%M:%S"
                            ts = mills.datetime2timestamp(pubdate, tformat=date_format)
                            pubdate = mills.timestamp2datetime(ts, tformat="%Y-%m-%d %H:%M:%S")
                        except Exception as e:
                            print('bad pubdate', pubdate, str(e))
                            pass
                    book_dict['date_added'] = pubdate
                if description:
                    description = description.text

                # http://libgen.rs/rss/index.php
                soup = BeautifulSoup(description, 'lxml')
                td_list = soup.find_all('td')
                num_of_td = len(td_list) if td_list else 0
                if num_of_td > 0 and num_of_td % 2 == 0:
                    for no_i in range(0, num_of_td, 2):
                        k = td_list[no_i].text.encode('utf-8').strip()
                        if not k:
                            continue

                        v = td_list[no_i + 1].text.encode('utf-8').strip()
                        if k.lower() in ['language:', 'date added:', 'size:', 'author:']:
                            k = k[0:-1]
                            k = k.lower()
                            k = k.replace(' ', '_')
                            v = strip_n(v)
                            book_dict[k] = v

                if title and link:
                    lan = book_dict.get('language')
                    if not lan:
                        lan = self.book_language_list[0]
                        book_dict['language'] = lan
                    if lan not in self.book_language_list:
                        continue
                    link = re.sub(r'\s+', '', link)
                    is_hit = self.is_security_book((title))
                    print(is_hit, title, link)
                    if not is_hit:
                        continue

                    title = strip_n(title)
                    book_dict['title'] = title
                    book_dict['link'] = link
                    date_added = book_dict.get('date_added')
                    if date_added:
                        book_dict['ts'] = date_added.replace("-", "")[0:8]
                    else:
                        book_dict['ts'] = mills.get_special_date(format="%Y%m%d")
                    # fill other field
                    field_list = ['author', 'size']
                    for field_name in field_list:
                        field_value = book_dict.get(field_name)
                        if not field_value:
                            book_dict[field_name] = "unknown"

                    sql = d2sql(book_dict, table='security_book', action='replace')
                    sql_list.append(sql)

            if sql_list:
                so = SQLiteOper("data/scrap.db")
                for sql in sql_list:
                    try:
                        so.execute(sql)

                    except Exception as e:
                        logging.error("[sql]: %s %s" % (sql, str(e)))

    def check_live(self, rss_url_list=None, proxy=None):
        """
        check which url is available
        """
        for rss_url in rss_url_list:
            s = requests.session()
            s.proxies = proxy
            r = s.request('GET', url=rss_url)
            if r.reason == "OK":
                print(rss_url, r)
                return rss_url
    def scaw(self, proxy=None):
        """

        :return:
        """
        if not self.rss_url_dict:
            return
        for rss_name, rss_url in self.rss_url_dict.items():
            if isinstance(rss_url, list):
                rss_url_list = rss_url
            else:
                rss_url_list = [rss_url]
            rss_url = self.check_live(rss_url_list, proxy=proxy)
            if not rss_url:
                continue
            day = timestamp2datetime(int(time.time()), tformat="%Y%m%d%H")
            fdir = os.path.join("data", "book")
            if not os.path.exists(fdir):
                os.mkdir(fdir)
            fname = os.path.join(fdir, "{rss_name}_{day}.xml".format(
                rss_name=rss_name,
                day=day
            ))
            is_need_down = False

            if not os.path.exists(fname):
                is_need_down = True
            else:
                if os.path.getsize(fname) == 0:
                    is_need_down = True
            if is_need_down:
                get_request(rss_url, proxy=proxy, fname=fname)

            if os.path.exists(fname):
                fname = os.path.abspath(fname)
                self.parse_xml(fname)


if __name__ == "__main__":
    """
    main
    """



    proxy = {
        "http": "http://127.0.0.1:8001",
        'https': "http://127.0.0.1:8001",
    }
    proxy = {
        "http": "http://127.0.0.1:1087",
        'https': "http://127.0.0.1:1087",
    }


    o = GetNewBook(proxy=proxy)
    o.scaw(proxy=proxy)
    title_list = [
        # 'Practical Cloud Security, 2nd Edition',
        #'CompTIA A+ Practice Test Core 1 (220-1101)',
        # 'Technology for Success and The Shelly Cashman Series Microsoft 365 & Office 2021 (MindTap Course List)',
    ]
    for title in title_list:
        is_hit = o.is_security_book(title)
        print('test', is_hit, title)
