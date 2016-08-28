# -*- coding: utf-8 -*-

'''
爬取：车站名称和车站编码，比如：上海：SH
'''

import scrapy
import json
from scrapy_12306.items import CommitItem
from scrapy_12306.items import StationTelecodeItem

class StationTelecodesSpider(scrapy.Spider):
    name = "station_telecode"
    start_urls = (
        'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8962/',
    )

    # 开启功能：中间件和过滤设置
    custom_settings = {
        # 'DUPEFILTER_DEBUG': True,
        'DOWNLOADER_MIDDLEWARES':{
            'scrapy_12306.middlewares.DownLoaderMiddleware': 500,
        },
        'DUPEFILTER_CLASS':"scrapy_12306.filter.URLTurnFilter",
        'JOBDIR': 'stop-break/station_telecode',
    }

    def __init__(self,*a,**kw):
        super(StationTelecodesSpider,self).__init__(self.name,**kw)
        self.turn = a[0]

    def parse(self, response):

        # 抽取所有的站点信息，包括了它的名称和telecode等其他一些信息
        stations = response.body.split('@')

        # 抽取站点的名字和telecode
        for station in stations:

            # 排除没有车站的data元素
            if '|' not in station:
                continue

            station_telecode_item = StationTelecodeItem()
            station_telecode_item['station_name'] = station.split('|')[1]
            station_telecode_item['station_telecode'] = station.split('|')[2]
            station_telecode_item['turn_id'] = self.turn
            yield station_telecode_item

        # 触发：提交数据库
        yield CommitItem()


