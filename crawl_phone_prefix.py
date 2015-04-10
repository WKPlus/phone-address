#!/usr/bin/env python
# -*- coding:utf8 -*-
import requests
import re
from bs4 import BeautifulSoup
import os
import time

URL = "http://www.nowdl.cn/city/guangdong/{}.php"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
}

CITY = {
    '广州': 'guangzhou', '湛江': 'zhanjiang',
    '肇庆': 'zhaoqing', '中山': 'zhongshan',
    '珠海': 'zhuhai', '潮州': 'chaozhou',
    '东莞': 'dongguan', '佛山': 'fushan',
    '河源': 'heyuan', '惠州': 'huizhou',
    '江门': 'jiangmen', '揭阳': 'jieyang',
    '茂名': 'maoming', '梅州': 'meizhou',
    '清远': 'qingyuan', '汕头': 'shantou',
    '汕尾': 'shanwei', '韶关': 'shaoguan',
    '深圳': 'shenzhen', '阳江': 'yangjiang',
    '云浮': 'yunfu',
}


def get_phone_prefix(cname, city, p=re.compile(r'^\d{7}$')):
    url = URL.format(city)
    r = requests.get(url)
    bs = BeautifulSoup(r.content)
    al = bs.find_all('a')
    ret = [i.get_text() for i in al if p.match(i.get_text())]
    print "%s爬取号码前缀%s个" % (cname, len(ret))
    return ret


if __name__ == '__main__':
    for cname, city in CITY.iteritems():
        ret = get_phone_prefix(cname, city)
        if os.path.isfile(city):
            continue
        with open(city, 'w') as out_fd:
            out_fd.write(cname)
            out_fd.write(" " + ",".join(ret))
            out_fd.write("\n")
        time.sleep(30)
