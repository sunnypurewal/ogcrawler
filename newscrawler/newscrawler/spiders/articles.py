# -*- coding: utf-8 -*-
import scrapy
import urllib
import dateparser
import datetime
import os
import json
import hashlib

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

class ArticleSpider(scrapy.Spider):
  name = "articlespider"

  def __init__(self, *args, **kwargs):
    super().__init__(kwargs)
    requests = []
    with open("../data/recent.urlset", "r") as f:
      line = f.readline()
      while(len(line) > 0):
        line = line.strip()
        obj = json.loads(line)
        # print(obj["loc"])
        requests.append(str(obj["loc"]))
        line = f.readline()
    self.start_urls = requests

  def next_request(self):
    print(self.f.tell())
    line = self.f.readline()
    obj = json.loads(line)
    print(self.f.tell())
    yield scrapy.Request(url=obj["loc"])

  def parse(self, response):
    ogtype = response.xpath("//meta[@property='og:type']/@content").get()
    item = self.parse_metadata(response)
    if ogtype == "article":
      self.parse_article(response, item)
    if ogtype == "video" or ogtype == "video.other":
      self.parse_video(response, item)
    return item

  def parse_metadata(self, response):
    item = Article()
    encodedurl = response.request.url.encode("utf-8")
    m = hashlib.sha256(encodedurl)
    id = m.hexdigest()
    item["url"] = response.request.url
    item["id"] = id
    published_time = response.xpath("//meta[@property='article:published_time'] | //meta[@property='og:article:published_time']").xpath("@content").get()
    if published_time is None or len(published_time) == 0:
      return        
    item["timestamp"] = int(dateparser.parse(published_time).timestamp())
    title = response.xpath("//meta[@property='og:title']/@content").get()
    if title is None or len(title) == 0:
      return
    item["title"] = title
    image = response.xpath("//meta[@property='og:image']/@content").get()
    if image is not None and len(image) > 0:
      item["imgurl"] = image
    description = response.xpath("//meta[@property='description']").get()
    if description is not None and len(description) > 0:
      item["description"] = description
    return item
  
  def parse_video(self, response, item):
    print("Video")
    return item

  
  def parse_article(self, response, item):
    paragraphs = response.xpath("//p")
    max = 0
    article = None
    for paragraph in paragraphs:
      siblings = paragraph.xpath("parent::*/child::p")
      if len(siblings) > max:
        max = len(siblings)
        article = paragraph.xpath("parent::*/child::p/text()").getall()
    # use article instead of paragraphs from now on
    print("Article")
    if article is not None and max > 0:
      charcount = 0
      wordcount = 0
      for p in article:
        charcount += len(p)
        wordcount += len(p.split(" "))
      if wordcount >= 150:
        item = self.parse_metadata(response)
        print("HERE")
        item["body"] = "\n".join(article)
        tags = response.xpath("//meta[@property='article:tag'] | //meta[@property='og:article:tag']")
        if tags is not None and len(tags) > 0:
          t = []
          for tag in tags:
            t.append(tag.xpath("@content").get().strip())
          item["tags"] = t
        else:
          tags = response.xpath("//meta[@property='article:tags'] | //meta[@property='og:article:tags']")
          if isinstance(tags, list):
            t = []
            for tagcsv in tags:
              for tagv in tagcsv.split(","):
                t.append(tagv.strip())
            item["tags"] = t
        author = response.xpath("//meta[@property='article:author'] | //meta[@property='article:author'] | //meta[@property='og:article:author'] | //meta[@property='og:article:author']").xpath("@content").get()
        if author is not None and len(author) > 0:
          item["author"] = author
        yield item
    # yield self.next_request()