# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
import scrapy
from scrapy_12306.items import AgencyItem
from scrapy_12306.items import CommitItem
from scrapy_12306.items import StationItem
from scrapy_12306.items import StationTelecodeItem
from scrapy_12306.items import TrainItem
from scrapy_12306.items import TrainTimeItem
from scrapy_12306.items import TurnItem


class Scrapy12306Pipeline(object):

    def __init__(self):

        # 连接数据库
        try:
            self.conn =pymysql.connect(host='localhost',port = 3306, user = 'linguoyang',password='816557',db = '12306',charset = 'utf8')
            self.cursor = self.conn.cursor()
        except Exception,e:
            print 'connect mysql:FAILED!'

        # 定义数据库语句：插入‘代售点’
        self.insert_agency_sql = "insert ignore agency_sellticket values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 定义数据库语句：插入‘车站’
        self.insert_stations_sql = "insert ignore stations VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        # 定义数据库语句：插入‘车站编码’
        self.insert_telecode_sql = "insert ignore station_telecodes VALUES(%s,%s,%s)"
        # 定义数据库语句：插入‘车次’
        self.insert_train_sql = "insert ignore trains VALUES(%s,%s,%s,%s,%s)"
        # 定义数据库语句：插入‘车次时刻表’
        self.insert_train_time_sql = "insert ignore train_time VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        # 定义数据库语句：插入‘时间标识’
        self.insert_turn_sql = "insert ignore turns VALUES(%s,%s)"

    def process_item(self, item, spider):

        # 接受到CommitItem指令，系统将提交数据库的执行动作
        if isinstance(item,CommitItem):
            try:
                self.conn.commit()
            except Exception, e:
                spider.logger.warning("commit fail!")

        # 将代售点的详细信息，插入到数据库中
        elif isinstance(item,AgencyItem):

            sta = self.cursor.execute(self.insert_agency_sql,\
                                      (item['agency_name'],\
                                        item['province'],\
                                        item['city'],\
                                        item['county'],\
                                        item['agency_address'],\
                                        item['start_time_am'],\
                                        item['stop_time_am'],\
                                        item['start_time_pm'],\
                                        item['stop_time_pm'], \
                                        item['turn_id'] \
                                       ))

        # 将代售点的详细信息，插入到数据库中
        elif isinstance(item,StationItem):

            sta = self.cursor.execute(self.insert_stations_sql,\
                                      (item['bureau'],\
                                        item['station_name'],\
                                        item['is_stop_point'],\
                                        item['station_address'],\
                                        item['service_stop'],\
                                        item['service_baggage'],\
                                        item['service_package'], \
                                        item['turn_id'] \
                                       ))

        # 将车站名称和车站编码，存入数据库
        elif isinstance(item,StationTelecodeItem):

            sta = self.cursor.execute(self.insert_telecode_sql,\
                                      (item['station_name'],\
                                        item['station_telecode'], \
                                        item['turn_id'] \
                                       ))

        # 将车次/车次编码/起点/终点，存入数据库
        elif isinstance(item,TrainItem):

            sta = self.cursor.execute(self.insert_train_sql,\
                                      (item['train_code'],\
                                        item['train_no'],\
                                        item['start_station_name'],\
                                        item['end_station_name'], \
                                        item['turn_id'] \
                                       ))

        # 将车次的详细时刻表，存入数据库
        elif isinstance(item,TrainTimeItem):

            sta = self.cursor.execute(self.insert_train_time_sql,\
                                      (item['train_code'],\
                                        item['train_no'],\
                                        item['station_name'],\
                                        item['arrive_time'],\
                                        item['start_time'],\
                                        item['station_no'],\
                                        item['stopover_time'],\
                                        item['turn_id']\
                                        ))


        return item
