# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy import signals
from scrapy import Request

from shops_scraper.util.proxy_db import ProxyDB


class ParsingSroSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        print('process_spider_output' + str(response.status))

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        print('process_spider_exception')
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ShopsScraperDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    proxy_list = ProxyDB.get_proxy_list()
    current_proxy = None
    working_proxy = set()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        request.meta['proxy'] = self.current_proxy
        request.meta['dont_redirect'] = True
        request.meta['download_timeout'] = 5
        print('proxy: ' + self.current_proxy)
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader
        print(response.status)
        if response.status != 200:
            print('proxy is change2')
            if len(self.proxy_list) > 0:
                self.current_proxy = self.proxy_list.pop()
            else:
                if len(self.working_proxy) > 0:
                    self.current_proxy = self.working_proxy.pop()
                else:
                    self.proxy_list = ProxyDB.get_proxy_list()
            request.meta['proxy'] = self.current_proxy
            request.meta['dont_redirect'] = True
            request.meta['download_timeout'] = 5
            return request
        else:
            self.working_proxy.add(request.meta['proxy'])
            return response
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        print('proxy is change')
        if len(self.proxy_list) > 0:
            self.current_proxy = self.proxy_list.pop()
        else:
            if len(self.working_proxy) > 0:
                self.current_proxy = self.working_proxy.pop()
            else:
                self.proxy_list = ProxyDB.get_proxy_list()
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        return request

    def spider_opened(self, spider):
        self.current_proxy = self.proxy_list.pop(0)
        spider.logger.info('Spider opened: %s' % spider.name)

