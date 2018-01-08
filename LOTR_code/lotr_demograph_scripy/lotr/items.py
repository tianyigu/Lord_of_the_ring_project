# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LotrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    race = scrapy.Field()
    gender = scrapy.Field()
    height = scrapy.Field()
    hair = scrapy.Field()
    spouse = scrapy.Field()
    birth = scrapy.Field()
    death = scrapy.Field()
    realm = scrapy.Field()