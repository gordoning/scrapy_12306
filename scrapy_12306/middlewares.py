# -*- coding: utf-8 -*-
from scrapy.exceptions import IgnoreRequest


class DownLoaderMiddleware(object):
    def process_request(self,request,spider):
        print u'忽烈忽烈忽烈'
        if 'turn' in request.meta:
            turn = request.meta['turn']

            if turn != spider.turn:
                print u'忽烈忽烈忽烈', turn, spider.turn
                raise IgnoreRequest()
            else:
                return None

        else:
            return None