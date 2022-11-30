import sqlite3
from sqlite3 import OperationalError
import databases

# Important: this file
db_path = None
tag = "[sql statement]: "
db_url = None


class DBService:

    async def open_connection(self):
        # Get connection of database
        db = databases.Database(self.db_url)
        await db.connect()
        return db
        # return await aiosqlite.connect(db_path)

    # ********************************** Public execute statement **********************************
    # ********************************** Note: Return only one record **********************************

    async def execute_sql_one(self, sql):
        db = await self.open_connection()
        print(tag, sql)
        return await db.fetch_one(sql)

    # ********************************** Public execute statement **********************************
    # ********************************** Note: Return only one record **********************************
    async def execute_sql_one_values(self, sql, values):
        db = await self.open_connection()
        print(tag, sql)
        return await db.fetch_one(sql, values)

    # ********************************** Public execute statement **********************************
    # ********************************** Note: Return only one record **********************************

    async def execute_sql_all(self, sql):
        db = await self.open_connection()
        print(tag, sql)
        return await db.fetch_all(sql)

    # ********************************** Public execute statement **********************************
    # ********************************** Note: Return only one record **********************************
    async def execute_sql_all_values(self, sql, values):
        db = await self.open_connection()
        print(tag, sql)

        return await db.fetch_all(sql, values)

    # ********************************** Public insert statement **********************************
    # ********************************** Note: Return the id if success **********************************
    async def insert(self, sql):
        db = await self.open_connection()
        # print(tag, sql)
        # Execute the sql statement
        return await db.execute(sql)

    # ********************************** Public update statement **********************************
    # ********************************** Note: Return id **********************************
    async def update(self, sql, values):
        db = await self.open_connection()
        print(tag, sql)
        return await db.execute(sql, values)

    # ********************************** Public update statement **********************************
    # ********************************** Note: Return a status **********************************

    def createTable(self, sql):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            print(sql)
            cursor.execute(sql)
            return True
        except OperationalError as o:
            pass
            print(o)
            return False
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            conn.close()

    # ********************************** Automatically **********************************
    # ********************************** Create db **********************************
    def createDB(self):
        print("############################## Initializing database... ##############################\n")
        print("Creating table ValidWords... ")
        sql = """CREATE TABLE ValidWords(id integer primary key, name varchar(128) not null, status integer defautlt '0');"""

        result = self.createTable(sql)
        if (result):
            print("Table ValidWords created.")

        print("Creating table Users... ")
        sql = """CREATE TABLE Users(username varchar(128) primary key, password varchar(128));"""

        result = self.createTable(sql)
        if (result):
            print("Table Users created.")

        print("Creating table Game... ")
        sql = """CREATE TABLE Game(game_id integer primary key, number_of_guesses integer, max_guess integer, status integer, username varchar(128) not null, secret_word_id integer not null, constraint fk_user foreign key (username) references User(username), constraint fk_valid_words foreign key (secret_word_id) references ValidWords(id) );"""

        result = self.createTable(sql)
        if (result):
            print("Table Game created.")

        print("Creating table Guess... ")
        sql = """CREATE TABLE Guess(id integer primary key, game_id integer not null, guessword_id integer not null, constraint fk_game foreign key (game_id) references Game(game_id), constraint fk_guess_valid_words foreign key (guessword_id) references ValidWords(id));"""
        result = self.createTable(sql)
        if (result):
            print("Table Guess created.")
        print("\n############################## Database has been created. ##############################\n")
