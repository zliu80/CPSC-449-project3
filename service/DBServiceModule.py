import itertools
import sqlite3
from itertools import cycle
from sqlite3 import OperationalError
import databases
from jedi.inference.value import iterable

# Important: this file

tag = "[sql statement]: "
db_write_url = None
db_urls = None


class DBService:
    it: iterable

    def __init__(self):
        self.db_read_url = None
        # Using iterools.cycle() to choose an url
        self.it = cycle(self.db_urls)

    async def open_read_connection(self):
        # Dynamically choose an url from primary and its replica.
        for i in self.it:
            self.db_read_url = i
            print("read from ", i)
            break

        db = databases.Database(self.db_read_url)
        await db.connect()
        return db
       
    
    async def open_write_connection(self):
        # Get connection of database
        db = databases.Database(self.db_write_url)
        print(tag, "open write connection")
        await db.connect()
        return db
        

    # ********************************** Public execute statement **********************************
    # ********************************** Note: Return only one record **********************************

    async def execute_sql_one(self, sql):
        db = await self.open_read_connection()
        print(tag, sql)
        return await db.fetch_one(sql)

    # ********************************** Public execute statement **********************************
    # ********************************** Note: Return only one record **********************************
    async def execute_sql_one_values(self, sql, values):
        db = await self.open_read_connection()
        print(tag, sql)
        return await db.fetch_one(sql, values)

    # ********************************** Public execute statement **********************************
    # ********************************** Note: Return only one record **********************************

    async def execute_sql_all(self, sql):
        db = await self.open_read_connection()
        print(tag, sql)
        return await db.fetch_all(sql)

    # ********************************** Public execute statement **********************************
    # ********************************** Note: Return only one record **********************************
    async def execute_sql_all_values(self, sql, values):
        db = await self.open_read_connection()
        print(tag, sql)

        return await db.fetch_all(sql, values)

    # ********************************** Public insert statement **********************************
    # ********************************** Note: Return the id if success **********************************
    async def insert(self, sql):
        db = await self.open_write_connection()
        print(tag, sql)
        return await db.execute(sql)

    # ********************************** Public update statement **********************************
    # ********************************** Note: Return id **********************************
    async def update(self, sql, values):
        db = await self.open_write_connection()
        print(tag, sql)
        return await db.execute(sql, values)

