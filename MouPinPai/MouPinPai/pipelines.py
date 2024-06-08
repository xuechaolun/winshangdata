# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MoupinpaiPipeline:
    # 爬虫启动时会自动调用一次该函数
    def open_spider(self, spider):
        if spider.name == 'winshangdata':
            self.mongo = pymongo.MongoClient(host='localhost', port=27017)
            self.coll = self.mongo['demo']['winshangdata']

    # 处理从爬虫文件传过来的item
    def process_item(self, item, spider):
        if spider.name == 'winshangdata':
            print(item)
            self.coll.insert_one(item)
        return item

    # 爬虫关闭时会自动调用一次该函数
    def close_spider(self, spider):
        if spider.name == 'winshangdata':
            self.mongo.close()
