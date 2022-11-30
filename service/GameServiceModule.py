from service.DBServiceModule import DBService

class GameService(DBService):

    def __init__(self):
        super(GameService, self).__init__()

    async def all_game(self, username):
        sql = "select * from Game where username =:username"
        values = {"username": username}
        rows = await self.execute_sql_all_values(sql, values)
        return rows

    # ********************************** Start a new game **********************************
    async def start_new_game(self, game):

        # Random pick a words as a secret word
        sql = 'select * from ValidWords where status = 1 order by random() limit 1'

        row = await self.execute_sql_one(sql)
        game.secret_word_id = row[0]
        args = [str(game.number_guesses), str(game.max_guess), str(game.status), game.username, game.secret_word_id]
        sql = 'insert into Game(number_of_guesses, max_guess, status, username, secret_word_id) Values(%s)'

        in_p = ', '.join(list(map(lambda x: "'%s'" % x, args)))
        sql = sql % in_p

        _id = await self.insert(sql)

        if (_id > 0):
            game.game_id = _id
            return game
        return None

    # ********************************** Retrieve a new game **********************************

    async def find_game_by_id(self, game_id):
        sql = "select * from Game where game_id =:game_id"
        values = {"game_id": game_id}
        row = await self.execute_sql_one_values(sql, values)
        return row

    # ********************************** Insert a new record to Guess table **********************************
    async def insert_guess(self, game_id, guessword_id):
        # Insert sql statement
        sql = "insert into Guess(game_id, guessword_id) Values('" + str(game_id) + "', '" + str(guessword_id) + "')"

        _id = await self.insert(sql)

        if _id > 0:
            return True
        return False

    # ********************************** Find a guess and return its id **********************************
    # Return the id if the record is found
    # Return 0 if the record is not found
    async def find_guess_name_by_word(self, word):
        # Select sql statement
        sql = "select * from ValidWords where name ='" + word + "'"
        row = await self.execute_sql_one(sql)

        return row

        # ********************************** Find a guess and return its id **********************************
        # Return the id if the record is found
        # Return 0 if the record is not found

    async def find_all_guess_by_game_id(self, game_id):
        # Select sql statement
        sql = "select * from Guess where game_id =:game_id"
        values = {"game_id": game_id}
        rows = await self.execute_sql_all_values(sql, values)

        return rows

    # ********************************** Find how many guesses a game made **********************************
    async def find_bumber_of_guess(self, game_id):
        # Select sql statement
        sql = "select count(*) from Guess where game_id = " + str(game_id)

        row = await self.execute_sql_one(sql)
        if row is None:
            return 0
        number_of_guesses = row[0]

        return number_of_guesses

    async def find_word_name_by_id(self, word_id):
        sql = "select name from ValidWords where id=:id"

        row = await self.execute_sql_one_values(sql, values={"id": word_id})
        if row is None:
            return None
        return row[0]

    async def update_game(self, game):
        sql = "update Game Set status = :status, number_of_guesses =:number_of_guesses where game_id = :game_id"
        values = {"status": game.status, "number_of_guesses": game.number_guesses, "game_id": game.game_id}
        row = await self.update(sql, values)
        if row is None:
            return False
        return True
