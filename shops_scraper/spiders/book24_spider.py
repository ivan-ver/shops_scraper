import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
from shops_scraper.items import book24_product


class Book24SpiderSpider(CrawlSpider):
    name = 'book24_spider'
    start_urls = ['http://book24.ru/catalog/']

    custom_settings = {
        "CONCURRENT_REQUESTS": 2,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=[
            "//a[@class='filter-item__link']"
        ]), callback='parse_category'),
    )

    def parse_category(self, response):
        links_ = LinkExtractor(restrict_xpaths=["//a[@class='book__image-link js-item-element ddl_product_link']"])\
            .extract_links(response)
        for url in links_:
            yield scrapy.Request(
                url=url.url,
                callback=self.parse_product
            )
        try:
            next_ = LinkExtractor(restrict_xpaths=["//a[text()='Далее']"]).extract_links(response)[0].url
            if next_:
                yield scrapy.Request(
                    url=next_,
                    callback=self.parse_category
                )
            else:
                return None
        except:
            return None

    @staticmethod
    def parse_product(response):
        product = book24_product()
        product['url'] = response.url
        js_info = [i for i in response.xpath("//script[@data-skip-moving='true']") if 'window.digitalData' in i.extract()][0]
        js_info = json.loads(js_info.xpath('text()').get().replace('window.digitalData = ', '')[:-1])
        product['title'] = js_info['product']['name']
        try:
            product['author'] = js_info['product']['author']
        except:
            product['author'] = None
        product['category'] = '>'.join(js_info['product']['category'])
        try:
            product['price'] = float(js_info['product']['unitSalePrice'])
        except:
            product['price'] = None
        product['ISBN'] = response.xpath("//div[@class='isbn js-copy-promocode']//input/@value").get()
        product['art'] = js_info['product']['id']
        return product
