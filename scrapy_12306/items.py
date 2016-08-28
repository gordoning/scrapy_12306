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
    agency_name = scrapy.Field()  #代售点名称,如：世家堂代售点
    province = scrapy.Field()  #省份，如：江苏
    city = scrapy.Field()   # 城市，如：苏州市
    county = scrapy.Field() # 地区，如：相城区
    agency_address = scrapy.Field() # 地址，如：江苏省苏州市相城区大城路112号
    start_time_am = scrapy.Field()  # 开始营业的时间，上午，如：8：12
    stop_time_am = scrapy.Field()   #  结束营业时间，上午
    start_time_pm = scrapy.Field()  # 开始营业时间，下午
    stop_time_pm = scrapy.Field()   # 结束营业时间，下午
    turn_id = scrapy.Field()  # 更新的标示，代表了某一次的更新


# 车站
class StationItem(scrapy.Item):
    bureau = scrapy.Field() # 铁路局名称，如：哈尔滨铁路局
    station_name = scrapy.Field()  # 站点名称，如：成春
    is_stop_point = scrapy.Field()  # 是否是乘降索，如：1表示是乘降所，0表示不是
    station_address = scrapy.Field()  # 地址，如：长春市大风区113号
    service_stop = scrapy.Field()  # 乘客乘降，如：1，表示是乘降，0表示不是
    service_baggage = scrapy.Field()  # 办理：行李，如：1表示办理行李，0标示不办理行李
    service_package = scrapy.Field()  # 办理：包裹，如：1表示办理包裹，0标示不办理
    turn_id = scrapy.Field()   #更新的标示，代表了某一次的更新


# 车站的编码
class StationTelecodeItem(scrapy.Item):
    station_name = scrapy.Field()   #站点名称，如北京
    station_telecode = scrapy.Field()   #站点编码，如BJ
    turn_id = scrapy.Field()  # 更新的标示，代表了某一次的更新


# 车次
class TrainItem(scrapy.Item):
    train_code = scrapy.Field()   #车次，如:D7037
    train_no = scrapy.Field()   #车次编码，如:12323232332
    start_station_name = scrapy.Field()   #起点,如：上海
    end_station_name = scrapy.Field()   #终点，如：武汉
    turn_id = scrapy.Field()   #更新的标示，代表了某一次的更新

# 车次时刻表
class TrainTimeItem(scrapy.Item):
    train_code = scrapy.Field()   #车站名称，如：D7037
    train_no = scrapy.Field()   #车站名称，如：12323232132
    station_name = scrapy.Field()   #车站名称，如：苏州
    arrive_time = scrapy.Field()   #到达时间，如：18：05
    start_time = scrapy.Field()   #开车时间，如：18：10
    station_no = scrapy.Field()   #车站序号，如：05
    stopover_time = scrapy.Field()   #停留时间，如：5分钟
    turn_id = scrapy.Field()   #更新的标示，代表了某一次的更新

# 更新的时间
class TurnItem(scrapy.Item):
    turn_id = scrapy.Field()    #更新标示，如：70470
    mark_time = scrapy.Field()  # 时间戳，如：2016-9-15 15：23：23

# 数据库提交，一旦Spider提交的是这个类，Pipline将触发一些特定的动作：比如存储数据库的执行
class CommitItem(scrapy.Item):
    pass