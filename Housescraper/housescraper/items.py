# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HouseItem(scrapy.Item):
    titre = scrapy.Field()
    prix = scrapy.Field()
    surface = scrapy.Field()
    chambres = scrapy.Field()
    ville = scrapy.Field()
    type_bien = scrapy.Field()
    type_transaction = scrapy.Field()
    source = scrapy.Field()
