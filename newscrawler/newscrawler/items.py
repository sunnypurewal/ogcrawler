# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
  id = scrapy.Field()
  title = scrapy.Field()
  description = scrapy.Field()
  body = scrapy.Field()
  url = scrapy.Field()
  imgurl = scrapy.Field()
  tags = scrapy.Field()
  timestamp = scrapy.Field()
  author = scrapy.Field()
  pass
