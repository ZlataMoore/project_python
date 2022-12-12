# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderCianItem(scrapy.Item):
    address = scrapy.Field()
    rooms = scrapy.Field()
    cost = scrapy.Field()
    details = scrapy.Field()
    coordinates = scrapy.Field()
    house = scrapy.Field()