# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from shops_scraper.util.parsing_db import ParsingDB


class ShopsScraperPipeline:
    db = ParsingDB()
    items = []
    flush_size = 10

    def open_spider(self, spider):
        self.db.connect()

    def close_spider(self, spider):
        self.db.save_all(self.items)
        self.db.disconnect()

    def process_item(self, item, spider):
        self.items.append(item)
        if len(self.items) == self.flush_size:
            self.db.save_all(self.items)
            self.items.clear()
        return item
