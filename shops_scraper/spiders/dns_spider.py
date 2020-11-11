import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from shops_scraper.items import dns_product


class DnsSpider(CrawlSpider):
    name = 'dns_spider'
    dns_url = 'https://www.dns-shop.ru'
    start_urls = ['https://www.dns-shop.ru/catalog/']
    pattern = "//li[@class='subcategory__childs-list-item']"
    custom_settings = {
        # "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS": 1
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=[pattern]), callback='second_level_parse'),
    )

    def second_level_parse(self, response):
        table_links = response.xpath("//a[@class='ui-link']/@href").extract()
        if len(table_links) == 0:
            second_level_links = response.xpath("//a[@class='subcategory__item ui-link ui-link_blue']//@href").extract()
            for url in second_level_links:
                yield self.get_request(
                    url=self.dns_url + url,
                    callback=self.second_level_parse
                )
        else:
            yield self.get_request(
                url=response.url,
                callback=self.product_list_parser
            )

    def product_list_parser(self, response):
        table_links = response.xpath("//div[@class='n-catalog-product__main']//a[@class='ui-link']/@href").extract()

        for url in table_links:
            yield self.get_request(
                url=self.dns_url + url,
                callback=self.product_parser
            )
        next_page = response.xpath("//li[@class='pagination-widget__page']/a/@href").extract()
        if next_page:
            yield self.get_request(
                    url=response.url + next_page[-1],
                    callback=self.product_list_parser,
                )
        else:
            return None

    @staticmethod
    def product_parser(response):
        product = dns_product()
        product['url'] = response.url
        product['title'] = response.xpath("//h1[@class='page-title price-item-title']/text()").get()
        product['category'] = ">".join(response.xpath("//ol[@class='breadcrumb-list']//span/text()")
                                       .extract()[1:-2]).replace("\n", "")
        product['brand'] = response.xpath("//div[@class='brand-logo']/a/img/@alt").get()
        product['code'] = response.xpath("//div[@class='price-item-code']/span/text()").get()
        try:
            js_tags = response.xpath("//script[@type='text/javascript']/text()").extract()
            js_tag = [i for i in js_tags if '"price":' in i][0]
            _obj = js_tag.split(',')
            _obj = [p for p in _obj if '"price":' in p][0]
            product['price'] = float(_obj.split(':')[1])
        except Exception:
            product['price'] = 0
        return product

    @staticmethod
    def get_request(url, callback, cb_kwargs=None):
        return scrapy.Request(
            url=url,
            callback=callback,
            cb_kwargs=cb_kwargs,
            dont_filter=True)

