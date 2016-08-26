# -*- coding: utf-8 -*-
import scrapy
import datetime
import urllib
import json
from scrapy_12306.items import CommitItem
from scrapy_12306.items import TrainItem



class TrainsSpider(scrapy.Spider):
    name = "trains"
    start_urls = (
        'https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?date=2016-05-01/',
    )



    def start_requests(self):
        self.headers =  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        # 定义所有车次的
        time = (datetime.datetime.now() + datetime.timedelta(days= 3)).strftime('%Y-%m-%d')
        url = 'https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?'  + urllib.urlencode({'date':time})

        # 请求所有车次的url
        yield scrapy.Request(url,headers= self.headers,callback=self.parse)

    def parse(self, response):
        # 解析车次列表
        trains = json.loads(response.body)['data']

        # 获取每个车次的信息，它的信息是{"station_train_code":"0000(沈阳-北京)","train_no":"120000421606"}
        for train in trains:

            # 分别截取车次/车次编码/起点/终点
            train_code = train['station_train_code'].split('(')[0]
            train_no = train['train_no']
            start_station_name = train['station_train_code'].split('(')[1].split('-')[0] #
            end_station_name = train['station_train_code'].split('(')[1].split('-')[1].replace(')','')

            # 将其存到item中
            train_item = TrainItem()
            train_item['train_code'] = train_code
            train_item['train_no'] = train_no
            train_item['start_station_name'] = start_station_name
            train_item['end_station_name'] = end_station_name

            yield train_item

        yield CommitItem()

