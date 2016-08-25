# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AgencyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    agency_name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    agency_address = scrapy.Field()
    start_time_am = scrapy.Field()
    stop_time_am = scrapy.Field()
    start_time_pm = scrapy.Field()
    stop_time_pm = scrapy.Field()

class CommitItem(scrapy.Item):
    pass