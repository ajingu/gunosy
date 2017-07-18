# -*- coding: utf-8 -*-
import pymysql


class Connect:
    def __init__(self):
        self.conn = pymysql.connect("localhost",
                                    "root",
                                    "guujin0120",
                                    "GunosyChallenge",
                                    charset="utf8")

        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def get_data(self):
        self.cursor.execute("SELECT * FROM clf_article")
        self.conn.commit()
        data = self.cursor.fetchall()
        if data:
            print("Successfully Downloaded")

        return data

    def delete_data(self):
        self.cursor.execute("DELETE FROM clf_article")
        self.cursor.execute("ALTER TABLE clf_article AUTO_INCREMENT = 0")
        self.conn.commit()
        print("Successfully Deleted")

    def close(self):
        self.conn.close()
        self.cursor.close()
        print("Successfully Closed")
