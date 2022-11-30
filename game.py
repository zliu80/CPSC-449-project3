from quart import Quart, request
import toml
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request
from service.GameServiceModule import GameService
from view.Game import Game
from service.DBServiceModule import DBService

# ************** Initialized variable **************#
app = Quart(__name__)
QuartSchema(app)

# For testing in pycharm
app.config.from_file(f"etc/game.toml", toml.load)
#app.config.from_file(f"etc/{__name__}.toml", toml.load)
DBService.db_url = app.config["DATABASES"]["URL"]
DBService.db_path = app.config['DATABASES']["DB_PATH"]
gameService = GameService()





# **************************************************************#
# **************************** Game ****************************#
# **************************************************************#

@app.route('/')
async def index():
    username = ""
    if request.authorization is not None:
    	    username = request.authorization.username   
    return {"authentificated user":username, "msg": "Welcome to the Wordle game. To play the game, you may visit http://tuffix-vm/docs to see the API, or see README.md"}
    
    
@app.route('/startgame')
async def start_new_game():
    msg = ""
    data = None
    username = None
    try:
        # Get the username from client
        
        #username = request.args.get('username')
        if request.authorization is not None:
    	    username = request.authorization.username  
        elif username is None:
            return {"msg": "To start a new game, the username must be provided."}

        # ******************** Project 2, User and Game Separate, so skip validation.

        # Check if the user is existed
        # user = await userService.find_user_by_name(username)
        # if user is None:
        #     return {"msg:" "The username you provided cannot be found."}



        game = Game(0, 0, app.config["GAME"]["MAX_GUESS"], 0, username, 0)
        # Call service module to start a new game
        new_game = await gameService.start_new_game(game)

        if new_game is None:
            msg = "Can't start a new game, something went wrong."
        else:
            msg = "success"
            game = await gameService.find_game_by_id(new_game.game_id)
            data = dict(game)
    except Exception as e:
        print(e)
        print("System error, please contact the author.")
    return {"msg": msg, "data": data}


def word_analysis(word, correct_word):
    list = []
    for i in range(len(word)):

        if word[i] == correct_word[i]:
            dct = {"correct_spot": {"letter": word[i], "letter_spot": i + 1, "letter_index": i}}
            list.append(dct)
        else:
            index = correct_word.find(word[i])
            if index != -1:
                dct = {"wrong_spot": {"letter": word[i], "letter_spot": i + 1, "letter_index": i}}
                list.append(dct)
    return list


@app.route('/guess')
async def guess():
    msg = ""
    words_analysis_list = None
    #username = request.args.get('username')
    username = None
    if request.authorization is not None:
    	    username = request.authorization.username  
    
    game_id = request.args.get("game_id")
    word = request.args.get('word')
    if username is None:
        return {"msg": "To guess a word, you must provide an username."}
    elif game_id is None:
        return {"msg": "To guess a word, You must provide the game id."}
    elif word is None:
        return {"msg": "You must guess a word."}
    elif len(word) != app.config["GAME"]["VALID_WORD_LENGTH"]:
        return {"msg": "The Administrator has set the word length must be " + str(
            app.config["GAME"]["VALID_WORD_LENGTH"])}
    try:

        # ******************** Project 2, User and Game Separate, so skip validation.

        # user = await userService.find_user_by_name(username)
        # if user is None:
        #     return {"msg": "The username you provided does not existed."}

        _game = await gameService.find_game_by_id(game_id)

        if _game is None:
            return {"msg": "The game cannot be found. You need to find out the game_id before guessing a word. List "
                           "all game: Try /allgame?username="}

        game = Game(_game['game_id'], _game['number_of_guesses'], _game['max_guess'], _game['status'],
                    _game['username'], _game['secret_word_id'])

        if username != game.username:
            return {"msg": "The game belongs to another user. You can't play others game."}

        if game.status == 1:
            return {"msg": "The game was finished. You won."}
        elif game.status == 2:
            return {"msg": "The game was finished. You lost."}
        # Count how many times the user has guessed
        guess_time = await gameService.find_bumber_of_guess(game_id)
        if guess_time >= game.max_guess:
            return {"msg": "The game was finished."}

        # 2. find if the word the user guess is valid word
        guessword_row = await gameService.find_guess_name_by_word(word)

        # To compare the secret_word_id
        if guessword_row is not None:
            guessword_id = guessword_row[0]
            # insert the new guess to the Guess table
            if await gameService.insert_guess(game.game_id, guessword_id):
                # To compare if the guess is a secret word
                game.number_guesses += 1
                if game.secret_word_id == guessword_id:
                    game.status = 1
                    msg = "Wowwwwwww! You won. The word you guessed is a secret word!"
                else:
                    remaining_time = game.max_guess - guess_time - 1
                    secret_word = await gameService.find_word_name_by_id(game.secret_word_id)
                    if remaining_time == 0:
                        game.status = 2
                        msg = "Oops! You lost. You've used up all your guesses. The secret word is " + secret_word
                    else:
                        msg = "Valid word, but not a secret word, you have " + str(remaining_time) + " times remaining."

                        words_analysis_list = word_analysis(word, secret_word)

                await gameService.update_game(game)
            else:
                msg = "Failed to insert the new guess."
        else:
            msg = "The word you guessed is not a valid word."
    except Exception as e:
        print(e)
        print("System error, please contact the author.")
    if words_analysis_list is not None and len(words_analysis_list) > 0:
        return {"msg": msg, "word_you_guess": word, "words_analysis": words_analysis_list}
    return {"msg": msg, "word_you_guess": word}


@app.route("/allgame")
async def allGame():
    listGame = []
    username = None
    try:
        #username = request.args.get('username')
        if request.authorization is not None:
    	    username = request.authorization.username  
        if username is None:
            return {"msg": "Require an username to do this search."}

        games = await gameService.all_game(username)
        listGame = list(map(dict, games))
    except Exception as e:
        print(e)
        print("System error, please contact the author.")
    if listGame is None:
        return {"msg": "success", "number_of_games": 0, "data": "none"}
    return {"msg": "success", "number_of_games": len(listGame), "data": listGame}


@app.route('/retrievegame')
async def retrieveGame():
    return_data = None
    try:
        game_id = request.args.get('game_id')
        if game_id is None:
            return {"msg": "To retrieve a game, the game_id is required."}

        _game = await gameService.find_game_by_id(game_id)
        if _game is None:
            return {"msg": "Could not find the game!"}
        game = dict(_game)

        secret_word = await gameService.find_word_name_by_id(game["secret_word_id"])

        _guesses = await gameService.find_all_guess_by_game_id(game_id)
        guesses = list(map(dict, _guesses))

        lst = []
        for g in guesses:
            guess_word_id = g["guessword_id"]
            word_name = await gameService.find_word_name_by_id(guess_word_id)
            lst.append({"word_name": word_name})

        if game["status"] == 0:
            game_status = "progressing"
        elif game["status"] == 1:
            game_status = "won"
        elif game['status'] == 2:
            game_status = "lost"
        else:
            game_status = "unknown"

        return_data = {"username": game["username"], "max_guess": game["max_guess"], "game_status": game_status,
                       "number_of_guess_you_made": game["number_of_guesses"], "guesses_you_made": lst,
                       "secret_word": secret_word}
    except Exception as e:
        print(e)
        print("System error, please contact the author.")
    return {"msg:": "success", "data": return_data}


@app.errorhandler(RequestSchemaValidationError)
def bad_request(e):
    return {"error": str(e.validation_error)}, 400


@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409


if __name__ == '__main__':
    try:

        if DBService.db_url is None or DBService.db_path is None:
            print("The system initialization failed! Check the db address.")

        app.run(debug=True)
    except Exception as e:
        print(e)
        print("The system initialization failed, please contact the author.")
