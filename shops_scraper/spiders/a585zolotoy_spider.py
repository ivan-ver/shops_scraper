from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from shops_scraper.items import a585zolotoy_product
import re


class A585zolotoySpiderSpider(CrawlSpider):
    name = '585zolotoy_spider'
    start_urls = ['http://585zolotoy.ru/catalog/']

    # custom_settings = {
    #     "DOWNLOAD_DELAY": 1,
    #     "CONCURRENT_REQUESTS": 2
    # }

    rules = (Rule(LinkExtractor(restrict_xpaths=[
        "//ul[@class='child-categories']/li/a",
    ]), callback='parse_category'),)

    def parse_category(self, response, page=1):
        links_ = LinkExtractor(restrict_xpaths=["//ul[@class='tiles']/li"]).extract_links(response)
        if links_:
            for url in links_:
                yield response.follow(
                    url=url.url,
                    callback=self.parse_product,
                    dont_filter=True
                )
            page += 1
            if re.search('/\d+/', str(response.url)):
                next_ = re.sub('/\d+/', '/{}/'.format(page), response.url)
            else:
                next_ = "{}{}/".format(str(response.url), page)
            yield response.follow(
                    url=next_,
                    callback=self.parse_category,
                    cb_kwargs={'page': page},
                    dont_filter=True
                )
        else:
            return None

    @staticmethod
    def parse_product(response):
        product = a585zolotoy_product()
        product['url'] = response.url
        product['title'] = response.xpath("//h1[@itemprop='name']/text()").get()
        product['category'] = '>'.join(response.xpath("//ul[@class='breadcrumbs no-margin-bottom']/li/a/text()")
                                       .extract())
        product['art'] = response.xpath("//div[@class='product-article']/span/text()").get()
        product['price'] = float(response.xpath("//div[@class='product-price']/span[@class='actual-price']/text()").get()[:-2].replace(" ", ""))
        product['material'] = response.xpath("//ul[@class='features-list']/li[contains (.,'Металл')]/div[2]//text()")\
            .get()
        return product

