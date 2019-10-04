import sys
import json
import logging
import os
from newscrawler.spiders.articles import ArticleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
  # logging.getLogger("scrapy").propagate = False


def geturls():

  # process = CrawlerProcess(get_project_settings())
  # process.crawl(ArticleSpider, name="articles", domains=politics)

  # print ("Starting Crawler Process")
  # process.start()

if __name__ == "__main__":
    main()
