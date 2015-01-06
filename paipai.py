#!/usr/bin/env python

import requests
import re
import random
import gevent
import sys
from gevent.threadpool import ThreadPool

CONCURRENCY = 60
URL_PREFIX = 'http://virtual.paipai.com/extinfo/GetMobileProductInfo?mobile={0}&amount={1}'
RESULT = []


def get_address(tel):
    amount = random.randint(10000, 20000)
    url = URL_PREFIX.format(tel, amount)
    res = requests.get(url)
    content = res.content.decode('gbk')
    province = re.search(r"province:'(.*?)'", content)
    city = re.search(r"cityname:'(.*?)'", content)
    if province and city:
        RESULT.append((tel, province.group(1), city.group(1)))

with open('tel') as in_fd:
    tel_list = [l.strip() for l in in_fd]

tp = ThreadPool(CONCURRENCY)
for tel in tel_list:
    tp.spawn(get_address, tel)

gevent.wait()

for r in RESULT:
    print r[0], r[1].encode('utf8'), r[2].encode('utf8')
