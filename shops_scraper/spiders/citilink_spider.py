import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from shops_scraper.items import citilink_product
from shops_scraper.util.parsing_db import ParsingDB


class CitilinkSpiderSpider(CrawlSpider):
    name = 'citilink_spider'
    start_urls = ['https://www.citilink.ru/catalog/']
    # url_list = ParsingDB().get_all_url('shops_scraper', 'citilink_product')

    custom_settings = {
        "DOWNLOAD_DELAY": 20,
        "CONCURRENT_REQUESTS": 2,
        # "ROTATING_PROXY_LIST": ProxyDB.get_proxy_list(),
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=[
            "//li[@class='CatalogLayout__children-item']",
            "//li[@class='CatalogLayout__children-item CatalogLayout__children-item_hideable "
            "CatalogLayout__children-item_hidden']"
        ]), callback='parse_category'),
    )

    def parse_category(self, response):
        table = response.xpath("//div[@class='ProductCardCategoryList__grid']").get()
        watch_all_products = response.xpath("//div[@class='main_content_inner']//h2//@href").extract()
        if table:
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_product_list,
                dont_filter=True,
                cb_kwargs={'page': 1},
            )
        elif watch_all_products:
            for url in watch_all_products:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_category,
                    dont_filter=True
                )
        else:
            return None

    def parse_product_list(self, response, page):
        product_list = LinkExtractor(restrict_xpaths=["//a[@class='ProductCardVertical__link link_gtm-js']"])\
            .extract_links(response)
        if product_list:
            for url in product_list:
                yield scrapy.Request(
                    url=url.url,
                    callback=self.parse_product,
                    dont_filter=True
                )
        else:
            return None
        page += 1
        if '?p=' in response.url:
            next_url = str(response.url).replace(str(response.url).split('?')[1], "p={}".format(page))
        else:
            next_url = str(response.url) + "?p={}".format(page)
        return scrapy.Request(
            url=next_url,
            callback=self.parse_product_list,
            cb_kwargs={'page': page}
        )

    @staticmethod
    def parse_product(response):
        product = citilink_product()
        json_info = response.xpath("//script[@type='application/ld+json']/text()").get()
        json_info = json.loads(json_info)
        product['url'] = response.url
        product['category'] = '>'.join([i.strip() for i in response.xpath("//div[@class='Breadcrumbs']/a//text()")
                                       .extract()])
        product['title'] = json_info['name']
        product['art'] = json_info['sku']
        product['brand'] = json_info['brand']
        product['price'] = float(json_info['offers']['price'])
        product['description_'] = json_info['description']
        return product
