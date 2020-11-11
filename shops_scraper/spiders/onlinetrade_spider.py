from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from shops_scraper.items import onlinetrade_product
from shops_scraper.util.parsing_db import ParsingDB


class OnlinetradeSpiderSpider(CrawlSpider):
    name = 'onlinetrade_spider'
    start_urls = ['http://www.onlinetrade.ru/catalogue']
    url_list = ParsingDB().get_all_url('shops_scraper', 'onlinetrade_product')

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=["//a[@class='iconedCategoriesItem__link black js__usualSpoilerLink']"]),
             callback='parse_category'),
    )

    def parse_category(self, response):
        product_list = response.xpath("//div[@class='indexGoods__item']").extract()
        links_ = LinkExtractor(restrict_xpaths=[
            "//div[@class='drawCats drawCats__dummyes']//a[@class='drawCats__item__link black']"
        ]).extract_links(response)

        if links_:
            for url in links_:
                yield response.follow(
                    url=url,
                    callback=self.parse_category)
        elif product_list:
            yield Request(
                url=response.url,
                callback=self.parse_product_list,
                dont_filter=True
            )

    def parse_product_list(self, response):
        links_ = LinkExtractor(restrict_xpaths=["//a[@class='indexGoods__item__image']"]).extract_links(response)
        if links_:
            for url in links_:
                if url.url not in self.url_list:
                    yield Request(
                        url=url.url,
                        callback=self.product_parse
                    )
        next_ = LinkExtractor(restrict_xpaths=["//a[@class='js__paginator__linkNext']"]).extract_links(response)
        if next_:
            return Request(
                url=next_[0].url,
                callback=self.parse_product_list
            )
        else:
            return None

    @staticmethod
    def product_parse(response):
        product = onlinetrade_product()
        product['url'] = response.url
        product['title'] = response.xpath("//div[@class='productPage__card']/h1/text()").get()
        product['category'] = '>'.join(response.xpath("//ul[@class='breadcrumbs__list']/li//span[1]/text()")
                                       .extract()[1:-2])
        product['brand'] = response.xpath("//ul[@class='breadcrumbs__list']/li//span[1]/text()").extract()[-2]
        product['code'] = response.xpath("//div[@class='descr__techicalBrand__line']/span[@class='nowrap']/text()")\
            .get()
        product['price'] = float(response.xpath("//span[@itemprop='price']/text()").get().replace(' ',''))
        return product
