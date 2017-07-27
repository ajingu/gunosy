# -*- coding: utf-8 -*-
import os
import pymysql


class Database:
    """Class that manages the interaction with the database."""
    def __init__(self):
        """Set cursor and connection."""
        self.conn = pymysql.connect(os.environ["GUNOSY_DATABASE_NAME"],
                                    os.environ["GUNOSY_USERNAME"],
                                    os.environ["GUNOSY_PASSWORD"],
                                    os.environ["GUNOSY_DATABASE_NAME"],
                                    charset="utf8")

        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

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