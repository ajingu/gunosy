# -*- coding: utf-8 -*-
import os
import pymysql


class Database:
    """Manage the interaction with the database."""

    def __init__(self):
        """Set cursor and connection."""
        self.conn = pymysql.connect(os.environ["GUNOSY__HOST"],
                                    os.environ["GUNOSY_USERNAME"],
                                    os.environ["GUNOSY_PASSWORD"],
                                    os.environ["GUNOSY_DATABASE_NAME"],
                                    charset="utf8")

        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        self.table_name = os.environ["GUNOSY_TABLE_NAME"]

    def delete_data(self):
        """Delete all rows from database."""
        self.cursor.execute("DELETE FROM %s", (self.table_name))
        self.cursor.execute("ALTER TABLE %s AUTO_INCREMENT = 0",
                            (self.table_name))
        self.conn.commit()
        print("Successfully Deleted")

    def close(self):
        """Close cursor and connection."""
        self.conn.close()
        self.cursor.close()
        print("Successfully Closed")
