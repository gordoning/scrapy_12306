# -*- coding: utf-8 -*-

'''
定义爬虫的url过滤条件：如果时间标示不变的话(一天内的时间标示，是一样的)，系统将自动过滤掉这条url
如果时间标示变化了（隔了一天或者几天后），系统将重新爬取这些url
'''

from scrapy.dupefilters import RFPDupeFilter

# 时间标示turn变化的话，返回的指纹信息就会变化，这就意味着：这个url会重新爬去
class URLTurnFilter(RFPDupeFilter):
    def request_fingerprint(self,request):
        if 'turn' in request.meta:
            return request.url + ("--%d"%request.meta['turn'])
        else:
            return request.url