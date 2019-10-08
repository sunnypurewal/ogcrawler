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

  def next_request(self):
    with open("data/recent.urlset", "r") as f:
      line = f.readline()
      obj = json.loads(line)
      yield scrapy.Request(url=obj["loc"])

  def start_requests(self):
    print ("Start Requests")
    return self.next_request()

  def parse(self, response):
    ogtype = response.xpath("//meta[@property='og:type']/@content").get()
    # if ogtype != "article": return
    paragraphs = response.xpath("//p")
    max = 0
    article = None
    for paragraph in paragraphs:
      siblings = paragraph.xpath("parent::*/child::p")
      if len(siblings) > max:
        max = len(siblings)
        article = paragraph.xpath("parent::*/child::p/text()").getall()
    #use article instead of paragraphs from now on
    print(article)
    if max > 0:
      charcount = 0
      wordcount = 0
      for p in article:
        charcount += len(p)
        wordcount += len(p.split(" "))
      if wordcount >= 150:
        encodedurl = response.request.url.encode("utf-8")
        m = hashlib.sha256(encodedurl)
        id = m.hexdigest()
        item = Article()
        item["body"] = "\n".join(article)
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
        yield self.next_request()