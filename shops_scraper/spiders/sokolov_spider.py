from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from shops_scraper.items import sokolov_product


class SokolovSpiderSpider(CrawlSpider):
    name = 'sokolov_spider'
    start_urls = ['http://sokolov.ru/']

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS": 2
    }

    rules = (Rule(LinkExtractor(restrict_xpaths=[
            "//a[text()='Кольца']",
            "//a[text()='Серьги']",
            "//a[text()='Цепи']",
            "//a[text()='Подвески']",
            "//a[text()='Браслеты']",
            "//a[text()='Колье']",
            "//a[text()='Посуда']",
            "//a[text()='Запанки']",
            "//a[text()='Пирсинг']",
            "//a[text()='Сувениры']",
        ]), callback='parse_category'),
    )

    def parse_category(self, response):
        product_list = LinkExtractor(restrict_xpaths=["//div[@class='product-list  ']"]).extract_links(response)
        for url in product_list:
            yield response.follow(
                url=url.url,
                callback=self.parse_product
            )
        next_ = LinkExtractor(restrict_xpaths=["//a[@class='right ']"]).extract_links(response)
        if next_:
            response.follow(
                url=next_[0].url,
                callback=self.parse_category
            )

    def parse_product(self, response):
        product = sokolov_product()
        product['url'] = response.url
        product['title'] = response.xpath("//h1[@class='product-title']/text()").get()
        product['category'] = '>'.join(response.xpath("//span[@class='breadcrumbs__item']//span/text()").extract()[1:])
        product['art'] = response.xpath("//div[@class='product-article']//text()").get().split(': ')[1]
        product['price'] = float(response.xpath("//span[@class='price']/@data-detail-price").get())
        return product

