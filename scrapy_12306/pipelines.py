# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
from scrapy_12306.items import AgencyItem
from scrapy_12306.items import CommitItem
from scrapy_12306.items import StationItem

class Scrapy12306Pipeline(object):

    def __init__(self):
        # print "init ok"
        self.conn =pymysql.connect(host='localhost',port = 3306, user = 'linguoyang',password='816557',db = '12306',charset = 'utf8')
        self.cursor = self.conn.cursor()
        # self.cursor.execute('select * from agency_sellticket')
        # print self.cursor.fetchone()
        self.insert_agency_sql = "insert ignore agency_sellticket(agency_name,province,city,county,agency_adress,start_time_am,stop_time_am,start_time_pm,stop_time_pm) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.insert_stations_sql = "insert ignore stations VALUES(%s,%s,%s,%s,%s,%s,%s)"

    def process_item(self, item, spider):
        if isinstance(item,CommitItem):
            self.conn.commit()

        elif isinstance(item,AgencyItem):
            #将代售点的详细信息，插入到数据库中
            sta = self.cursor.execute(self.insert_agency_sql,\
                                      (item['agency_name'],\
                                        item['province'],\
                                        item['city'],\
                                        item['county'],\
                                        item['agency_address'],\
                                        item['start_time_am'],\
                                        item['stop_time_am'],\
                                        item['start_time_pm'],\
                                        item['stop_time_pm']\
                                        ))

        elif isinstance(item,StationItem):
            print item['station_address']
            #将代售点的详细信息，插入到数据库中
            sta = self.cursor.execute(self.insert_stations_sql,\
                                      (item['bureau'],\
                                        item['station_name'],\
                                        item['is_stop_point'],\
                                        item['station_address'],\
                                        item['service_stop'],\
                                        item['service_baggage'],\
                                        item['service_package']\
                                        ))

        return item
