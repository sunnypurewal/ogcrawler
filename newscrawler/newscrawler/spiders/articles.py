# -*- coding: utf-8 -*-
import scrapy
import datetime
import dateparser
import json
import sys
import os

class ArticleSpider(scrapy.Spider):
  name = 'articles'

  def start_requests(self):
    with open("domains.json", "r") as f:
      domains = json.load(f)
    print (domains)

  def parse(self, response):
    pass
