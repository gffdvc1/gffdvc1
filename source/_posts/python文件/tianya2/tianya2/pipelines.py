# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from tianya2.ty2 import Ty2Spider.redis

class Tianya2Pipeline:
    def process_item(self, item, spider):
        dic = {item["title"]:item["content"]}
        if self.redis.sismember("detail_content",dic):
            print("已经添加到rdisl")
        else:
            self.redis.sadd("detail_content",dic)
            print("储存到数据库~~~~")
            
