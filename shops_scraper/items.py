import scrapy


class dns_product(scrapy.Item):
    url = scrapy.Field()        # varchar(255)
    title = scrapy.Field()      # varchar(255)
    category = scrapy.Field()   # varchar(255)
    brand = scrapy.Field()      # varchar(255)
    code = scrapy.Field()       # varchar(255)
    price = scrapy.Field()      # float


class sportmaster_product(scrapy.Item):
    url = scrapy.Field()        # varchar(255)
    title = scrapy.Field()      # varchar(255)
    brand = scrapy.Field()      # varchar(255)
    price = scrapy.Field()      # float
    type = scrapy.Field()       # varchar(255)


class wildberies_roduct(scrapy.Item):
    url = scrapy.Field()        # varchar(255)
    title = scrapy.Field()      # varchar(255)
    category = scrapy.Field()   # varchar(255)
    art = scrapy.Field()        # varchar(255)
    brand = scrapy.Field()      # varchar(255)
    price = scrapy.Field()      # float


class eldorado_product(scrapy.Item):
    url = scrapy.Field()        # varchar(255)
    title = scrapy.Field()      # varchar(255)
    category = scrapy.Field()   # varchar(255)
    art = scrapy.Field()        # varchar(255)
    brand = scrapy.Field()      # varchar(255)
    price = scrapy.Field()      # float


class citilink_product(scrapy.Item):
    url = scrapy.Field()        # varchar(255)
    title = scrapy.Field()      # varchar(255)
    category = scrapy.Field()   # varchar(255)
    art = scrapy.Field()        # varchar(255)
    brand = scrapy.Field()      # varchar(255)
    price = scrapy.Field()      # float
    description_ = scrapy.Field()


class book24_product(scrapy.Item):
    url = scrapy.Field()  # varchar(255)
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    ISBN = scrapy.Field()
    art = scrapy.Field()
    price = scrapy.Field()


class detmir_product(scrapy.Item):
    url = scrapy.Field()  # varchar(255)
    title = scrapy.Field()  # varchar(255)
    category = scrapy.Field()  # varchar(255)
    art = scrapy.Field()  # varchar(255)
    brand = scrapy.Field()  # varchar(255)
    price = scrapy.Field()  # float


class onlinetrade_product(scrapy.Item):
    url = scrapy.Field()        # varchar(255)
    title = scrapy.Field()      # varchar(255)
    category = scrapy.Field()   # varchar(255)
    brand = scrapy.Field()      # varchar(255)
    code = scrapy.Field()       # varchar(255)
    price = scrapy.Field()      # float


class sokolov_product(scrapy.Item):
    url = scrapy.Field()  # varchar(255)
    title = scrapy.Field()  # varchar(255)
    category = scrapy.Field()  # varchar(255)
    art = scrapy.Field()  # varchar(255)
    price = scrapy.Field()  # float


class a585zolotoy_product(scrapy.Item):
    url = scrapy.Field()  # varchar(255)
    title = scrapy.Field()  # varchar(255)
    category = scrapy.Field()  # varchar(255)
    art = scrapy.Field()  # varchar(255)
    price = scrapy.Field()  # float
    material = scrapy.Field()
