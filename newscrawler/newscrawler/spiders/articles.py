# -*- coding: utf-8 -*-
import scrapy
import urllib
import dateparser
import datetime
import os
import json

class ArticleSpider(scrapy.Spider):
  name = "articlespider"

  def start_requests(self):
    print ("Start Requests")
    for filename in os.listdir("data/urlsets"):
      path = os.path.join("data/urlsets", filename)
      f = open(path)
      line = f.readline()
      while len(line) > 0:
        obj = json.loads(line)
        line = f.readline()
        yield scrapy.Request(url=obj["loc"])

  # def parse(self, response):
  #   links = response.xpath("//a")
  #   print (f"{response.request.url} {len(links)} <a> elements")
  #   for link in links:
  #     url = link.xpath("@href").get()
  #     urlcomponents = urllib.parse.urlparse(url)
  #     if len(urlcomponents.scheme) > 0:
  #       yield(scrapy.Request(url=url, 
  #                            callback=self.parse_article))
  #     elif len(urlcomponents.path) > 0:
  #       yield(scrapy.Request(url=f"{response.request.url}{urlcomponents.path}", 
  #                            call
  #back=self.parse_article))

  def parse(self, response):
    ogtype = response.xpath("//meta[@property='og:type']/@content").get()
    # if ogtype != "article": return
    paragraphs = response.xpath("//p")
    candidatep = None
    for paragraph in paragraphs:
      siblings = paragraph.xpath("following-sibling::p")
      print(f"This p has {len(siblings)} siblings")
    print(paragraphs)