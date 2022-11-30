import sqlite3
from sqlite3 import OperationalError
import databases

# Important: this file

tag = "[sql statement]: "
db_write_url = None
db_read_url1 = None
db_read_url2 = None


class DBService:

    async def open_read_connection(self):
        # Get connection of database
        db = databases.Database(self.db_read_url1)
        print(tag, "open read connection")

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

