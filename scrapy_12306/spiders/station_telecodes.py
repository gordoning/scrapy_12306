# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_12306.items import CommitItem
from scrapy_12306.items import StationTelecodeItem



class StationTelecodesSpider(scrapy.Spider):
    name = "station_telecodes"
    start_urls = (
        'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8962/',
    )

    def parse(self, response):
        # 所有的站点信息，包括了它的telecode
        stations = response.body.split('@')

        # 抽取站点的名字和telecode
        for station in stations:
            if '|' not in station:
                continue

            station_telecode_item = StationTelecodeItem()
            station_telecode_item['station_name'] = station.split('|')[1]
            station_telecode_item['station_telecode'] = station.split('|')[2]
            yield station_telecode_item

        yield CommitItem()


