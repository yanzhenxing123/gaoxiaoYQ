import os
import time

while True:
    os.system("scrapy crawl weibo")
    time.sleep(24 * 60 * 60)

