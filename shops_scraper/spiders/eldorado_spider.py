from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
from shops_scraper.items import eldorado_product
from shops_scraper.util.parsing_db import ParsingDB


class EldoradoSpiderSpider(CrawlSpider):
    name = 'eldorado_spider'
    start_urls = ['https://www.eldorado.ru']
    all_urls = ParsingDB().get_all_url("shops_scraper", "eldorado_product")

    rules = (
        Rule(LinkExtractor("/d/[A-Za-z]"), callback='parse_category'),
    )

    def parse_category(self, response):
        urls = LinkExtractor(restrict_xpaths=["//a[@class='sc-1tqvus8-7 dVVFmE']"]).extract_links(response)
        for url in urls:
            yield response.follow(
                url=url.url,
                callback=self.parse_product_list)

    def parse_product_list(self, response):
        urls = LinkExtractor(restrict_xpaths=["//a[@class='sc-1w9a1pg-13 sc-19ibhqc-14 iLOHAr']"]).extract_links(response)
        for url in urls:
            if url.url not in self.all_urls:
                yield response.follow(
                    url=url.url,
                    callback=self.parse_product
                )
        _next = response.xpath("//li[@class='next']//@href").get()
        if _next:
            return Request(
                url=self.start_urls[0] + _next,
                callback=self.parse_product_list
            )
        else:
            return None

    @staticmethod
    def parse_product(response):
        product = eldorado_product()
        product['url'] = response.url
        data_layer = [i.strip()
                      for i in response.xpath("//script[@type='text/javascript']/text()").extract()
                      if 'dataLayer' in i][0][16:].split(';')[0]
        data_layer = json.loads(data_layer)[0]
        product['title'] = data_layer['productName']
        product['category'] = data_layer['breadCrumbs'].replace('/', '>')
        product['art'] = data_layer['ecommerce']['detail']['products']['id']
        product['brand'] = data_layer['ecommerce']['detail']['products']['brand']
        product['price'] = float(data_layer['ecommerce']['detail']['products']['price'])
        return product
