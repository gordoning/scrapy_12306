# -*- coding: utf-8 -*-

from scrapy.dupefilters import RFPDupeFilter


class URLTurnFilter(RFPDupeFilter):
    def request_fingerprint(self,request):
        if 'turn' in request.meta:
            print u'重复重复重复重复'
            return request.url + ("--%d"%request.meta['turn'])
        else:
            return request.url