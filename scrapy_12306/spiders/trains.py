# -*- coding: utf-8 -*-

'''
1，爬取所有车次和车次编号
2，爬去每个车次的时刻表
'''


import scrapy
import datetime
import urllib
import json
import time
from scrapy_12306.items import CommitItem
from scrapy_12306.items import TrainItem
from scrapy_12306.items import TrainTimeItem
from scrapy_12306.items import TurnItem


class TrainsSpider(scrapy.Spider):
    name = "trains"
    start_urls = (
        'https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?date=2016-05-01/',
    )

    # 开启功能：中间件和过滤设置
    custom_settings = {
        # 'DUPEFILTER_DEBUG': True,
        'DOWNLOADER_MIDDLEWARES':{
            'scrapy_12306.middlewares.DownLoaderMiddleware': 500,
        },
        'DUPEFILTER_CLASS':"scrapy_12306.filter.URLTurnFilter",
        'JOBDIR': 'stop-break/trains',
    }

    # 初始化Spider，将时间标示turn传入进来
    def __init__(self,*a,**kw):
        super(TrainsSpider,self).__init__(self.name,**kw)
        self.turn = a[0]

    # 开始第一个url的请求
    def start_requests(self):

        self.headers =  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        # 确定：‘3天后所有车次’的url
        time = (datetime.datetime.now() + datetime.timedelta(days= 3)).strftime('%Y-%m-%d')
        trains_url = 'https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?'  + urllib.urlencode({'date':time})

        # 请求：‘获取所有车次’的url
        yield scrapy.Request(trains_url,headers= self.headers,meta= {'turn':self.turn}, callback=self.trains_parse)

    # 抓取每个车次的信息，包括：车次，车次编号，出发站点，终点站点
    def trains_parse(self, response):

        # 解析车次列表
        trains = json.loads(response.body)['data']

        # i =0
        # j =0

        # 获取每个车次的简单信息，原始信息是这样的：{"station_train_code":"0000(沈阳-北京)","train_no":"120000421606"}
        for train in trains:

            # 分别截取车次/车次编码/起点/终点
            train_code = train['station_train_code'].split('(')[0]
            train_no = train['train_no']
            start_station_name = train['station_train_code'].split('(')[1].split('-')[0] #
            end_station_name = train['station_train_code'].split('(')[1].split('-')[1].replace(')','')

            # 将其存到TrainItem中
            train_item = TrainItem()
            train_item['train_code'] = train_code
            train_item['train_no'] = train_no
            train_item['start_station_name'] = start_station_name
            train_item['end_station_name'] = end_station_name
            train_item['turn_id'] = self.turn
            yield train_item

            # 调试用的
            # i=i+1
            # if i>2:
            #     break

        # 将车次信息，全部提交Pipleline
        yield CommitItem()

        # 依次获取每个“车次时刻表”的url
        for train in trains:
            train_code = train['station_train_code'].split('(')[0]
            train_no = train['train_no']
            time = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%Y-%m-%d')
            url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?' + \
                  urllib.urlencode({'train_no':train_no}) + '&'+ \
                  urllib.urlencode({'from_station_telecode':'BBB'}) + '&'+ \
                  urllib.urlencode({'to_station_telecode':'BBB'}) + '&'+ \
                  urllib.urlencode({'depart_date':time})

            # 请求url：这个车次的详细时刻表
            yield scrapy.Request(url,
                                 headers=self.headers,
                                 meta={'train_code':train_code,
                                       'train_no':train_no,
                                       'turn':self.turn
                                       },
                                 callback=self.train_time_parse)

            # j=j+1
            # if j>2:
            #     break

    #解析：某个车次的详细时刻表，同时触发数据库的执行动作
    def train_time_parse(self,response):

        train_times = json.loads(response.body)['data']['data']

        for train_time in train_times:
            train_time_item = TrainTimeItem()
            train_time_item['train_code'] = response.meta['train_code']
            train_time_item['train_no'] = response.meta['train_no']
            train_time_item['station_name'] = train_time['station_name']
            train_time_item['arrive_time'] = train_time['arrive_time']
            train_time_item['start_time'] = train_time['start_time']
            train_time_item['station_no'] = train_time['station_no']
            train_time_item['stopover_time'] = train_time['stopover_time']
            train_time_item['turn_id'] = self.turn

            yield train_time_item

        yield CommitItem()



