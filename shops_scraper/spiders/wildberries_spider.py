import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from shops_scraper.items import wildberies_roduct


class WildberriesSpider(CrawlSpider):
    name = 'wildberries_spider'
    start_urls = ['http://www.wildberries.ru']
    schema = "//ul[@class='topmenus']/li/a[text()='{}']"

    custom_settings = {
        "CONCURRENT_REQUESTS": 4
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=[
            schema.format("Мужчинам"),
            schema.format("Женщинам"),
            schema.format("Детям"),
            schema.format("Аксессуары"),
            schema.format("Спорт"),
            schema.format("Электроника"),
            schema.format("Бытовая техника"),
            schema.format("Книги"),
            schema.format("Красота"),
            schema.format("Игрушки"),
            schema.format("Продукты"),
            schema.format("Зоотовары"),
            schema.format("Канцтовары"),
            schema.format("Здоровье"),
            schema.format("Для ремонта"),
            schema.format("Дом"),
            schema.format("Автотовары"),
            schema.format("Ювелирные изделия"),
            schema.format("Подарки "),
            schema.format("Товары для взрослых"),
        ]), callback='category_parser'),
    )

    def category_parser(self, response):
        if 'sport' in response.url:
            pattern = "//ul[@class='maincatalog-list-1']//li//@href"
        else:
            pattern = "//div[@class='left']//li[not(@*)]//@href"
        parent_links = response.xpath(pattern).extract()
        child_links = response.xpath("//li[@class='selected hasnochild']/ul/li//@href").extract()
        if len(parent_links) != 0:
            for url in parent_links:
                yield response.follow(url=url, callback=self.category_parser)
        elif len(child_links) != 0:
            for url in child_links:
                yield response.follow(url=url, callback=self.category_parser)
        else:
            yield self.get_request(url=response.url, callback=self.product_list_parser)

    def product_list_parser(self, response):
        for url in response.xpath("//div[@class='catalog_main_table j-products-container']//a/@href").extract():
            category = '>'.join(response.xpath("//ul[@class='bread-crumbs']//span/text()").extract()[1:])
            yield self.get_request(url=self.start_urls[0] + url, callback=self.product_parser, cb_kwargs={'category': category})
        next_ = response.xpath("//a[@class='pagination-next']/@href").get()
        if next_:
            yield response.follow(url=next_, callback=self.product_list_parser)

    @staticmethod
    def product_parser(response, category):
        product = wildberies_roduct()
        product['url'] = response.url
        product['title'] = response.xpath("//div[@class='brand-and-name j-product-title']/span/text()").extract()[1].strip()
        product['category'] = category
        product['art'] = response.xpath("//div[@class='article']/span/text()").get()
        product['brand'] = response.xpath("//div[@class='brand-and-name j-product-title']/span/text()").extract()[0]
        price = response.xpath("//div[@class='final-price-block']/span/text()").get()
        try:
            product['price'] = float("".join(re.findall("\d+", price)))
        except:
            product['price'] = None
        return product

    @staticmethod
    def get_request(url, callback, cb_kwargs=None):
        return scrapy.Request(
            url=url,
            callback=callback,
            cb_kwargs=cb_kwargs,
            dont_filter=True
        )
