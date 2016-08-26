# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#代售点
class AgencyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    agency_name = scrapy.Field()  #代售点名称
    province = scrapy.Field()  #省份
    city = scrapy.Field()   # 城市
    county = scrapy.Field() # 地区
    agency_address = scrapy.Field() # 地址
    start_time_am = scrapy.Field()  # 开始营业的时间，上午
    stop_time_am = scrapy.Field()   #  结束营业时间，上午
    start_time_pm = scrapy.Field()  # 开始营业时间，下午
    stop_time_pm = scrapy.Field()   # 结束营业时间，下午

# 车站
class StationItem(scrapy.Item):
    bureau = scrapy.Field() # 铁路局
    station_name = scrapy.Field()  # 站点名称
    is_stop_point = scrapy.Field()  # 是否是乘降索
    station_address = scrapy.Field()  # 地址
    service_stop = scrapy.Field()  # 乘客乘降
    service_baggage = scrapy.Field()  # 办理：行李
    service_package = scrapy.Field()  # 办理：包裹

# 数据库提交
class CommitItem(scrapy.Item):
    pass