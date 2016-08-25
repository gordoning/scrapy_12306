# -*- coding: utf-8 -*-
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

    def start_requests(self):
        self.headers =  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        # self.cookie = {'bid':'ID7V121y-F8', 'll':"118163", 'ct':'y', '_pk_id.100001.4cf6':'2e0009b8aa8bc2e2.1470575800.5.1470657979.1470650297.', 'ap':'1'}
        yield scrapy.Request('https://kyfw.12306.cn/otn/userCommon/allProvince', headers= self.headers, callback=self.city_parse)

    def city_parse(self, response):

        provinces = json.loads(response.body)['data']
        # self.logger.debug(provinces);

        for province in provinces:
            province_name = province["chineseName"]
            url = "https://kyfw.12306.cn/otn/queryAgencySellTicket/queryAgentSellCity?"
            province_name_url = urllib.urlencode({"province":province_name.encode('utf-8')})
            citys_url = url + province_name_url
            return scrapy.Request(citys_url,headers=self.headers,meta= {'province':province_name},callback=self.country_parse)


    def country_parse(self,response):

        cities = json.loads(response.body)['data']

        for city in cities:
            city_name = city[0]
            url = 'https://kyfw.12306.cn/otn/queryAgencySellTicket/queryAgentSellCounty?'

            city_name_url = urllib.urlencode({'province':response.meta['province'].encode('utf-8'), \
                                                 'city':city_name.encode('utf-8')})
            city_url = url + city_name_url

            return scrapy.Request(city_url, headers=self.headers, \
                                 meta={'province':response.meta['province'],'city':city_name},\
                                 callback=self.agency_parse)

    def agency_parse(self,response):

        counties = json.loads(response.body)['data']

        for county in counties:
            county_name = county[0]
            url = 'https://kyfw.12306.cn/otn/queryAgencySellTicket/query?'

            county_name_url = urllib.urlencode({'province':response.meta['province'].encode('utf-8'), \
                                                'city':response.meta['city'].encode('utf-8'),\
                                                 'county':county_name.encode('utf-8')})
            county_url = url + county_name_url
            print '@@@@@@@@@@@@@@@@@'*5+county_url

            return scrapy.Request(county_url, headers=self.headers, \
                                 meta={'province':response.meta['province'],'city':response.meta['city'], 'county':county_name},\
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
            # print agency_item
            yield agency_item
        yield CommitItem()