# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

conf = {
    'baidu_nlp_account': {

        "app_id": '',
        "api_key": '',
        "secret_key": ''
    },
    'nlp_pos_dict': {  # 词性字典
        'n': '普通名词',
        'nr': '人名',
        'nz': '其他专名',
        'ns': '地名',
        'nt': '机构团体名',
        'an': '名形容词',
        'nw': '作品名',
        'vn': '动名词',
        'f': '方位名词',
        's': '处所名词',
        't': '时间名词',
        'a': '形容词',
        'm': '数量词',
        'c': '连词',
        'v': '普通动词',
        'ad': '副形词',
        'q': '量词',
        'u': '助词',
        'r': '代词',
        'xc': '其他虚词',

    },
    "category_data": {
        '漏洞分析': ['cve', 'poc', '0day', 'exploit', 'fuzz', 'shell', 'pwn', 'exp', 'shellcode',
                 '远程代码执行漏洞'],
        '移动安全': ['Android', 'iOS', '安卓', 'app', 'USB'],
        '物联网安全': ['物联网', 'IoT', 'PLC', 'ISC'],
        '数据挖掘': ['机器学习', 'AI', 'Elasticsearch', '大数据', '深度学习', 'Spark',
                 'hadoop', 'TensorFlow', 'NLP', '自然语言处理', 'Splunk',
                 'Kaggle', 'DGA'],
        'Web安全': ['XSS', 'SQL注入', 'web安全'
                                  'webshell',
                  'bypass', 'RCE', 'XXE', 'SSRF', 'getshell'],
        '工具': ['tools', 'Metasploit', 'BurpSuit', 'IDA',
               '漏洞扫描器', 'sqlmap', '树莓派', 'SyScan',
               'Kali Linux'],
        '会议比赛': ['CTF', 'PPT', 'PDF', 'RSA', 'Blackhat',
                 'DEF CON', 'Videos', '沙龙', 'DEFCON', 'slide',
                 'SANS', 'ACM CCS', 'report'],
        '威胁分析': ['APT', 'NSA', 'malware', 'SMB', 'Wanna'],
        '网络安全': ['DNS', 'HTTPS', 'VPN', 'Tor', 'SSL', 'DDoS', '中间人攻击', 'GSM'],
        '服务器安全': ['MySQL', 'Oracle', 'MongoDB', 'Apache', 'docker', 'Nginx', 'Tomcat', 'SSH'],
        '威胁情报': ['子域名', 'Malware', 'Mirai', '病毒', 'Threat', 'Shodan', 'Intelligence'],
        '安全检测': ['代码审计', 'WAF', 'SIEM', 'SOC'],
        '资料': ['awesome'],
        '比特币': ['以太坊', '比特币']

    }
}
