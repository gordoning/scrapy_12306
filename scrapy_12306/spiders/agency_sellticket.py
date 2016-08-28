# -*- coding: utf-8 -*-

'''
爬取所有代售点的信息，包括省份，城市，地区，代售点名称，地址, 营业时间等
'''

import scrapy
import json
import urllib
from scrapy_12306.items import AgencyItem
from scrapy_12306.items import CommitItem


class AgencySellticketSpider(scrapy.Spider):
    name = "agency_sellticket"
    start_urls = (
        'http://www.https://kyfw.12306.cn/otn/queryAgencySellTicket/init/',
    )

    # 开启功能：中间件,过滤设置,断点续传
    custom_settings = {
        # 'DUPEFILTER_DEBUG': True,
        'DOWNLOADER_MIDDLEWARES':{
            'scrapy_12306.middlewares.DownLoaderMiddleware': 500,
        },
        'DUPEFILTER_CLASS':"scrapy_12306.filter.URLTurnFilter",
        'JOBDIR':'stop-break/agency',   # 断点续传：已经爬取过的url，将不再重复爬取
    }

    # 构造函数，将时间标示turn传入进来
    def __init__(self,*a,**kw):
        super(AgencySellticketSpider,self).__init__(self.name,**kw)
        self.turn = a[0]

    #第一次请求http
    def start_requests(self):
        self.headers =  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        yield scrapy.Request('https://kyfw.12306.cn/otn/userCommon/allProvince',meta={'turn':self.turn}, headers= self.headers, callback=self.city_parse)

    #通过省份，请求它包含的所有城市
    def city_parse(self, response):

        provinces = json.loads(response.body)['data']
        # self.logger.debug(provinces);

        for province in provinces:
            province_name = province["chineseName"]
            url = "https://kyfw.12306.cn/otn/queryAgencySellTicket/queryAgentSellCity?"
            province_name_url = urllib.urlencode({"province":province_name.encode('utf-8')})
            citys_url = url + province_name_url
            yield scrapy.Request(citys_url,headers=self.headers,meta= {'province':province_name,'turn':self.turn},callback=self.country_parse)

    # 通过城市，获取它所有的地区
    def country_parse(self,response):

        cities = json.loads(response.body)['data']

        for city in cities:
            city_name = city[0]
            url = 'https://kyfw.12306.cn/otn/queryAgencySellTicket/queryAgentSellCounty?'
            city_name_url = urllib.urlencode({'province':response.meta['province'].encode('utf-8'), \
                                                 'city':city_name.encode('utf-8')})
            city_url = url + city_name_url
            yield scrapy.Request(city_url, headers=self.headers, \
                                 meta={'province':response.meta['province'],'city':city_name,'turn':self.turn},\
                                 callback=self.agency_parse)

    # 通过省份，城市，地区，获取这个地区下边的所有代售点
    def agency_parse(self,response):

        counties = json.loads(response.body)['data']

        for county in counties:
            county_name = county[0]
            url = 'https://kyfw.12306.cn/otn/queryAgencySellTicket/query?'
            county_name_url = urllib.urlencode({'province':response.meta['province'].encode('utf-8'), \
                                                'city':response.meta['city'].encode('utf-8'),\
                                                 'county':county_name.encode('utf-8')})
            county_url = url + county_name_url

            yield scrapy.Request(county_url, headers=self.headers, \
                                 meta={'province':response.meta['province'],'city':response.meta['city'], 'county':county_name, 'turn':self.turn},\
                                 callback=self.agency_detail_parse)

    def agency_detail_parse(self,response):

        agencies = json.loads(response.body)['data']['datas']
        for agency in agencies:
            agency_item = AgencyItem()
            agency_item['agency_name'] = agency['agency_name']
            agency_item['province'] = response.meta['province']
            agency_item['city'] = response.meta['city']
            agency_item['county'] = response.meta['county']
            agency_item['agency_address'] = agency['address']
            agency_item['start_time_am'] = agency['start_time_am']
            agency_item['stop_time_am'] = agency['stop_time_am']
            agency_item['start_time_pm'] = agency['start_time_pm']
            agency_item['stop_time_pm'] = agency['stop_time_pm']
            agency_item['turn_id'] = self.turn
            yield agency_item

        yield CommitItem()