# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymysql


class GunosynewsPipeline(object):
    """Pipeline that interacts with the database."""
    def __init__(self):
        """Set cursor and connection."""
        self.conn = pymysql.connect(os.environ["GUNOSY_HOST"],
                                    os.environ["GUNOSY_USERNAME"],
                                    os.environ["GUNOSY_PASSWORD"],
                                    os.environ["GUNOSY_DATABASE_NAME"],
                                    charset="utf8")

        self.cursor = self.conn.cursor()

        table = os.environ["GUNOSY_TABLE_NAME"]
        self.cmd = "INSERT INTO " + table + " (text, category) VALUES (%s, %s)"

    def process_item(self, item, spider):
        """Upload the scraped item."""
        try:
            self.cursor.execute(
                self.cmd,
                (item["text"], item["category"])
            )

            self.conn.commit()

        except Exception as e:
            print("Error: {0}".format(e))

        return item

    def close_spider(self, spider):
        """Close cursor and connection."""
        self.cursor.close()
        self.conn.close()
