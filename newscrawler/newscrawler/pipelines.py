# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html



# class JSONOutputPipeline(object):

#   @classmethod
#   def from_crawler(cls, crawler):
#     return cls(
#       path=crawler.settings.get("OUTPUT_PATH")
#     )
#   def __init__(self, path):
#     self.path = path
#     self.q = []
#     self.i = 0

#   def open_spider(self, spider):
#     logger = logging.getLogger("newscrawler")
#     if not os.path.exists(self.path):
#       logger.debug("Creating output path at ", self.path)
#       os.mkdir(self.path)
#     for filename in os.listdir(self.path):
#       splitext = os.path.splitext(filename)
#       if splitext[-1] != ".jsonlines": continue
#       t = int(splitext[0].split("-")[-1])
#       if t > self.i: self.i = t
#     logger.debug(f"Creating output file at {self.path}/articles-{self.i}.jsonlines")
#     self.file = open(f"/{self.path}/articles-{self.i}.jsonlines", 'w+')

#   def close_spider(self, spider):
#     self.file.close()

#   def process_item(self, item, spider):
#     logger = logging.getLogger("newscrawler")
#     self.q.append(f"{json.dumps(dict(item))}\n")
#     if len(self.q) > 25:
#       logger.info("Flushing items queue to file")
#       if self.file.tell() > 1000000:
#         self.file.close()
#         self.i += 1
#         self.file = open(f"{self.path}/articles-{self.i}.jsonlines", "w")
#       self.file.writelines(self.q)
#       self.q = []
#     return item