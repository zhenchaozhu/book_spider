# coding: utf-8

import subprocess
import os
from datetime import datetime
out_log = 'biquge-%s.log' % datetime.now().strftime('%Y-%m-%d-%M-%S')
out_log_path = os.path.join('/data/spider_log', out_log)
os.chdir('/home/ubuntu/opt/book_spider')
with open(out_log_path, 'wb') as out:
    subprocess.Popen(["scrapy", "crawl", "biquge"], stdout=out, stderr=out)