#!/usr/bin/env python

import requests
import re
import gevent
from gevent.threadpool import ThreadPool

CONCURRENCY = 1
URL_PREFIX = 'http://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel='
RESULT = []


def get_address(tel):
    url = URL_PREFIX + tel
    res = requests.get(url)
    ret = re.search(r"province:'(.*?)'", res.content.decode('gbk'))
    if ret:
        RESULT.append((tel, ret.group(1)))

with open('tel') as in_fd:
    tel_list = [l.strip() for l in in_fd]

tp = ThreadPool(CONCURRENCY)
for tel in tel_list[2000:]:
    tp.spawn(get_address, tel)

gevent.wait()

for r in RESULT:
    print r[0], r[1].encode('utf8')
