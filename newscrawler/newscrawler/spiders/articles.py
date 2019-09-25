# -*- coding: utf-8 -*-
import scrapy
import urllib
import dateparser
import datetime

class ArticleSpider(scrapy.Spider):

  def __init__(self, name=None, *args, **kwargs):
    super().__init__(name, *args, **kwargs)
    self.domains = kwargs["domains"]

  def start_requests(self):
    return [scrapy.Request(url=f"https://www.{d}") for d in self.domains]

  def parse(self, response):
    links = response.xpath("//a")
    print (f"{response.request.url} {len(links)} <a> elements")
    for link in links:
      url = link.xpath("@href").get()
      urlcomponents = urllib.parse.urlparse(url)
      if len(urlcomponents.scheme) > 0:
        yield(scrapy.Request(url=url, 
                             callback=self.parse_article))
      elif len(urlcomponents.path) > 0:
        yield(scrapy.Request(url=f"{response.request.url}{urlcomponents.path}", 
                             callback=self.parse_article))

  def parse_article(self, response):
    ogtype = response.xpath("//meta[@property='og:type']/@content").get()
    if ogtype != "article": return
    paragraphs = response.xpath("//p")
    for paragraph in paragraphs:
      siblings = paragraph.xpath("following-sibling::p")
      print(f"This p has {len(siblings)} siblings")