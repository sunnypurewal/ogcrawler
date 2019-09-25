import sys
import json
import logging
from newscrawler.spiders.articles import ArticleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main(domainsfile):
  logging.getLogger("scrapy").propagate = False
  with open(domainsfile, "r") as f:
    domains = json.loads(f.read())
    politics = domains["politics"]

  process = CrawlerProcess(get_project_settings())
  process.crawl(ArticleSpider, name="articles", domains=politics)

  print ("Starting Crawler Process")
  process.start()

if __name__ == "__main__":
    main(sys.argv[1])
