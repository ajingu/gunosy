# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class GunosynewsPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect("localhost", 
                                    "root", 
                                    "guujin0120", 
                                    "GunosyChallenge", 
                                    charset="utf8")
        
        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):
        try:
            self.cursor.execute("INSERT INTO clf_article (title, text, category) VALUES (%s, %s, %s)", 
                                (item["title"], item["text"], item["category"]))
            
            self.conn.commit()
            
            
        except Exception as e:
            print("Error: {0}".format(e))
            
            
        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
