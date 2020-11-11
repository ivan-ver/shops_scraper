import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import json

from shops_scraper.items import detmir_product


class DetmirSpiderSpider(CrawlSpider):
    name = 'detmir_spider'
    start_urls = ['https://www.detmir.ru']
    main_url = 'https://www.detmir.ru'
    rules = (
        Rule(LinkExtractor(restrict_xpaths=["//a[@class='_Ge' "
                                            "and not (text()='') "
                                            "and not (text()='Акции')]"
                                            ]), callback='parse_category'),
    )

    def parse_category(self, response):
        links_ = LinkExtractor(restrict_xpaths=["//a[@class='_au']"]).extract_links(response)
        for url in links_:
            yield scrapy.Request(
                url=url.url,
                callback=self.parse_product_list
            )

    def parse_product_list(self, response):
        product_list = LinkExtractor(restrict_xpaths=["//a[@class='tF tq']"]).extract_links(response)
        links_ = LinkExtractor(restrict_xpaths=["//a[@class='_BB _aM']"]).extract_links(response)
        if product_list:
            for url in product_list:
                yield scrapy.Request(
                    url=url.url,
                    callback=self.parse_product
                )
        elif links_:
            for url in links_:
                yield scrapy.Request(
                    url=url.url,
                    callback=self.parse_product_list
                )
        next_ = LinkExtractor(
            restrict_xpaths=["//div[@class='BU gc bG bD BZ bh bg bo']//a[@class='AN']"])\
            .extract_links(response)
        if next_:
            yield scrapy.Request(
                url=next_[0].url,
                callback=self.test
            )
        else:
            return None

    def test(self, response):
        r=response

    @staticmethod
    def parse_product(response):
        json_info = response.xpath("//script[@type='application/ld+json']/text()").get()
        json_info = json.loads(json_info)
        product = detmir_product()
        product['url'] = response.url
        product['title'] = json_info['name']
        product['price'] = float(json_info['offers']['price'])
        product['art'] = json_info['mpn']
        product['brand'] = json_info['brand']['name']
        product['category'] = '>'.join(response.xpath("//li[@class='sC']//text()").extract()[1:])
        return product


