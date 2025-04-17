from core.model import database
import sqlite3
import logging

from logger_ import logger

class sqlite(database):
    def __init__(self, database):
        self.database = database
        logger.info(f"Initializing SQLite database connection for {database}")
        self.conn = self.get_conn()

    def get_conn(self):
        try:
            conn = sqlite3.connect(self.database)
            logger.info("Successfully established SQLite database connection")
            return conn
        except Exception as e:
            error_msg = f"Cannot get the connection for the sqlite3: {e}"
            logger.error(error_msg)
            return error_msg

    def get_data(self, sql_query):
        conn=self.conn
        try:
            logger.info(f"Executing SQL query: {sql_query}")
            data=conn.execute(sql_query)
            logger.info("Successfully executed SQL query")
            return data
        except Exception as e:
            error_msg = f"Failed to execute the sql_query: {e}"
            logger.error(error_msg)
            return error_msg
