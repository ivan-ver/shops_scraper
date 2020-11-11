from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from shops_scraper.items import sportmaster_product


class SportmasterSpider(CrawlSpider):
    name = 'sportmaster_spider'
    start_urls = ['http://www.sportmaster.ru/catalog/']
    pattern = "//div[@class='sm-infopage sm-infopage-pagecat newLayout']//h3"

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS": 2
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=[pattern]), callback='category_parser'),
    )

    def category_parser(self, response):
        product_table = LinkExtractor(restrict_xpaths=["//div[@class='sm-category__items-wrap clearfix']//h2"])\
            .extract_links(response)
        subcategory_table = LinkExtractor(restrict_xpaths=["//table[@class='sm-subcategory__content']//h2"]).extract_links(response)
        if len(product_table) != 0:
            yield self.get_request(url=response.url, callback=self.product_list_parser)
        elif len(subcategory_table) != 0:
            for url in subcategory_table:
                yield response.follow(url=url.url, callback=self.category_parser)

    def product_list_parser(self, response):
        product_table = LinkExtractor(restrict_xpaths=["//div[@class='sm-category__items-wrap clearfix']//h2"]) \
            .extract_links(response)
        for url in product_table:
            yield self.get_request(url=url.url, callback=self.product_parser)
        next_ = response.xpath("//div[@class='sm-category__main-sorting_pager']/a[@rel='next']/@href").get()
        if next_:
            yield response.follow(url=next_, callback=self.product_list_parser)

    @staticmethod
    def product_parser(response):
        product = sportmaster_product()
        product['url'] = response.url
        product['title'] = response.xpath("//div[@class='sm-goods_main_details']/h1/text()").get()
        product['brand'] = response.xpath("//div[@class='sm-goods_main_photos-block']//a//@alt").get()
        product['price'] = float(response.xpath("//meta[@itemprop='price']/@content").get())
        product['type'] = '>'.join(response.xpath("//div[@class='sm-breadcrumbs']/a/text()").extract())
        return product

    @staticmethod
    def get_request(url, callback, cb_kwargs=None):
        return Request(
            url=url,
            callback=callback,
            cb_kwargs=cb_kwargs,
            dont_filter=True
        )


