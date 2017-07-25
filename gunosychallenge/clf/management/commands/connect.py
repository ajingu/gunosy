# -*- coding: utf-8 -*-
import pymysql


class Connect:
    """Class that manages the interaction with the database."""
    def __init__(self):
        """Set cursor and connection."""
        self.conn = pymysql.connect("localhost",
                                    "root",
                                    "guujin0120",
                                    "GunosyChallenge",
                                    charset="utf8")

        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def get_data(self):
        """Fetch all rows from database."""
        self.cursor.execute("SELECT DISTINCT * FROM clf_article")
        self.conn.commit()
        data = self.cursor.fetchall()
        if data:
            print("Successfully Downloaded")

        else:
            print("Data is nothing")

        return data

    def delete_data(self):
        """Delete all rows from database."""
        self.cursor.execute("DELETE FROM clf_article")
        self.cursor.execute("ALTER TABLE clf_article AUTO_INCREMENT = 0")
        self.conn.commit()
        print("Successfully Deleted")

    def close(self):
        """Close cursor and connection."""
        self.conn.close()
        self.cursor.close()
        print("Successfully Closed")
