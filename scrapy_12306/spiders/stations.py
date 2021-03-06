# -*- coding: utf-8 -*-

'''
爬虫：所有车站的信息，包括车站名称，办理包裹，办理行李等信息
'''

import scrapy
import json
import urllib
from bs4 import BeautifulSoup
from scrapy_12306.items import StationItem
from scrapy_12306.items import CommitItem


class ScrapyStationsSpider(scrapy.Spider):
    name = "stations"
    start_urls = (
        'http://www.12306.cn/mormhweb/kyyyz/',
    )

    # 开启功能：中间件和过滤设置
    custom_settings = {
        # 'DUPEFILTER_DEBUG': True,
        'DOWNLOADER_MIDDLEWARES':{
            'scrapy_12306.middlewares.DownLoaderMiddleware': 500,
        },
        'DUPEFILTER_CLASS':"scrapy_12306.filter.URLTurnFilter",
        'JOBDIR': 'stop-break/stations',
    }

    def __init__(self,*a,**kw):
        super(ScrapyStationsSpider,self).__init__(self.name,**kw)
        self.turn = a[0]


    # 获取所有的铁路局，并发起请求：车站详情和乘降所的详情
    def parse(self, response):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        # 创建一个HTML解析器
        soup = BeautifulSoup(response.body,'lxml')
        bereaus = soup.select('#secTable > tbody > tr > td')
        bereau_urls = soup.select('#mainTable td.submenu_bg > a')

        # 获取每个铁路局下面的车站地址和乘降所的地址
        for i in range(0,len(bereaus)):

            bereau_url1 = 'http://www.12306.cn/mormhweb/kyyyz' + bereau_urls[i*2]['href'][1:]  # 每一个铁路局下的车站地址
            bereau_url2 = 'http://www.12306.cn/mormhweb/kyyyz' + bereau_urls[i*2 + 1]['href'][1:]  # 每一个铁路局下的乘降所地址

            yield scrapy.Request(bereau_url1,
                                 headers=self.headers,
                                 meta= {'bereau':bereaus[i].text, 'is_stop_point':0, 'turn':self.turn},
                                 callback=self.station_parse)
            yield scrapy.Request(bereau_url2,
                                 headers=self.headers,
                                 meta={'bereau': bereaus[i].text, 'is_stop_point': 1, 'turn':self.turn},
                                 callback=self.station_parse)

    # 获取每个站点的详细信息
    def station_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        stations = soup.select('table table tr')

        for station in stations:
            # 忽烈前两行没有实际数据的td
            if not station.find_all('td'):
                continue
            station_item = StationItem()
            station_item['bureau'] = response.meta['bereau']
            station_item['station_name'] = station.find_all('td')[0].text
            station_item['is_stop_point'] = response.meta['is_stop_point']
            station_item['station_address'] = station.find_all('td')[1].text
            if station.find_all('td')[2].text.strip() != '':
                station_item['service_stop'] = 1
            else:
                station_item['service_stop'] = 0

            if station.find_all('td')[3].text.strip() != '':
                station_item['service_baggage'] =1
            else:
                station_item['service_baggage'] =0

            if station.find_all('td')[4].text.strip() != '':
                station_item['service_package'] = 1
            else:
                station_item['service_package'] = 0
            station_item['turn_id'] = self.turn

            yield station_item

        yield CommitItem()



