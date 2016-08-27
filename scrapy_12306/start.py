# coding:utf-8

import os
import sys
import time
import datetime
import pymysql

project_path = os.path.dirname(os.path.abspath(__file__+'/..'))
sys.path.insert(0,project_path)

from spiders.agency_sellticket import AgencySellticketSpider
from spiders.station_telecode import StationTelecodesSpider
from spiders.stations import ScrapyStationsSpider
from spiders.trains import TrainsSpider


# scrapy api imports
from twisted.internet import  reactor
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.utils import defer



# 设置爬虫启动配置
settings = get_project_settings()
crawler = CrawlerProcess(settings)





# 按顺序执行每一个spider
@defer.defer.inlineCallbacks
def crawl():

    turn = int(time.time() / 86400)  # 设置时间代码，当天内任何时候的时间代码是一样的；但过了一天后，turn将加上1
    mark_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 当天的时间戳

    # 连接数据库，将时间戳插入进入
    conn = pymysql.connect(host='localhost', port=3306, user='linguoyang', password='816557', db='12306',
                           charset='utf8')
    with conn.cursor() as cursor:
        insert_turn_sql = "insert ignore turns VALUES(%s,%s)"
        sta = cursor.execute(insert_turn_sql, \
                             (turn, \
                              mark_time \
                              ))
    conn.commit()
    conn.close()

    yield crawler.crawl(AgencySellticketSpider,turn)
    yield crawler.crawl(StationTelecodesSpider,turn)
    yield crawler.crawl(ScrapyStationsSpider,turn)
    yield crawler.crawl(TrainsSpider,turn)

crawl()
crawler.start()

