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
    turn_id = scrapy.Field()  # 更新的标示，代表了某一次的更新


# 车站
class StationItem(scrapy.Item):
    bureau = scrapy.Field() # 铁路局
    station_name = scrapy.Field()  # 站点名称
    is_stop_point = scrapy.Field()  # 是否是乘降索
    station_address = scrapy.Field()  # 地址
    service_stop = scrapy.Field()  # 乘客乘降
    service_baggage = scrapy.Field()  # 办理：行李
    service_package = scrapy.Field()  # 办理：包裹
    turn_id = scrapy.Field()   #更新的标示，代表了某一次的更新


# 车站的编码
class StationTelecodeItem(scrapy.Item):
    station_name = scrapy.Field()   #站点名称
    station_telecode = scrapy.Field()   #站点编码
    turn_id = scrapy.Field()  # 更新的标示，代表了某一次的更新


# 车次
class TrainItem(scrapy.Item):
    train_code = scrapy.Field()   #车次
    train_no = scrapy.Field()   #车次编码
    start_station_name = scrapy.Field()   #起点
    end_station_name = scrapy.Field()   #终点
    turn_id = scrapy.Field()   #更新的标示，代表了某一次的更新

# 车次时刻表
class TrainTimeItem(scrapy.Item):
    train_code = scrapy.Field()   #车站名称
    train_no = scrapy.Field()   #车站名称
    station_name = scrapy.Field()   #车站名称
    arrive_time = scrapy.Field()   #到达时间
    start_time = scrapy.Field()   #开车时间
    station_no = scrapy.Field()   #车站序号
    stopover_time = scrapy.Field()   #停留时间
    turn_id = scrapy.Field()   #更新的标示，代表了某一次的更新

# 更新的时间
class TurnItem(scrapy.Item):
    turn_id = scrapy.Field()
    mark_time = scrapy.Field()  # 时间戳

# 数据库提交
class CommitItem(scrapy.Item):
    pass