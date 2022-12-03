import json

import databases
import quart
from quart import Quart, request, render_template, abort, current_app
import toml
from quart_schema import QuartSchema, validate_request
import redis

app = Quart(__name__)

QuartSchema(app)

app.config.from_file(f"etc/leaderboard.toml", toml.load)

tag = "Leaderboard -> Game [sql statement]: "
db_url = app.config["DATABASES"]["URL"]


@app.route('/post')
async def post():
    # Find all won game with status = 1
    won = await find_all_won_game()
    # Find all won game with status = 2
    lost = await find_all_lost_game()
    # Redis Connection Pool
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # delete all rank in the past.
    r.zremrangebyrank("board", 0, -1)

    # Accumulated score
    for row in won:
        username = row[0]
        number_of_guesses = row[1]
        # score formula: score = won in 1 guess = 6, won in 2 guesses = 5, and so on. So score = 7 - number of guesses
        new_score = 7 - number_of_guesses
        r.zincrby("board", new_score, username)

    for row in lost:
        username = row[0]
        # Lost game gets a 0 score
        r.zincrby("board", 0, username)
    return {"status" : "success", "msg" : "All scores are posted. See Top 10 at http://tuffix-vm/rank"}

@app.route('/rank')
async def rank():
    # Redis Connection Pool
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    # Get the rank data from Redis
    data = dict(r.zrevrange("board", 0, 9, withscores=True))
    # Print the rank data
    app.logger.info(data)
    # Generate a return json data
    result = {"status" : "success", "msg" : "Listing the top 10 average scores.", "rank_data" : data}
    # return {"data" : data} will sort the data
    # This response type won't sort the scores.
    return quart.Response(json.dumps(result), mimetype='application/json')

async def find_all_won_game():
    # Insert sql statement
    sql = "select username, number_of_guesses from Game where status = 1"
    app.logger.info(sql)
    return await execute_sql_all(sql)

async def find_all_lost_game():
    # Insert sql statement
    sql = "select username, number_of_guesses from Game where status = 2"
    app.logger.info(sql)
    return await execute_sql_all(sql)


# ********************************** Public SQL statement **********************************

async def open_connection():
    # Get connection of database
    db = databases.Database(db_url)
    await db.connect()
    return db
    # return await aiosqlite.connect(db_path)


# ********************************** Public execute statement **********************************
# ********************************** Note: Return only one record **********************************

async def execute_sql_all(sql):
    db = await open_connection()
    print(tag, sql)
    return await db.fetch_all(sql)


# ********************************** Public execute statement **********************************
# ********************************** Note: Return only one record **********************************

async def execute_sql_one(sql):
    db = await open_connection()
    print(tag, sql)
    return await db.fetch_one(sql)


# ********************************** Public insert statement **********************************
# ********************************** Note: Return the id if success **********************************
async def insert(sql):
    db = await open_connection()
    # print(tag, sql)
    # Execute the sql statement
    return await db.execute(sql)


# ********************************** Public update statement **********************************
# ********************************** Note: Return id **********************************
async def update(sql, values):
    db = await open_connection()
    print(tag, sql)
    return await db.execute(sql, values)


# @app.errorhandler(RequestSchemaValidationError)
def bad_request(e):
    return {"error": str(e.validation_error)}, 400


@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409


if __name__ == '__main__':
    try:

        app.run(debug=True)
    except Exception as e:
        print(e)
        print("The system initialization failed, please contact the author.")
