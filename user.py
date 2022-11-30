import dataclasses

import quart
from quart import Quart, request, render_template, abort, current_app
import toml
from quart_schema import QuartSchema, validate_request

# from quart_schema import QuartSchema, RequestSchemaValidationError
from service.UserServiceModule import UserService

from service.DBServiceModule import DBService
from view.User import User

# ************** Initialized variable **************#
app = Quart(__name__)

QuartSchema(app)

DBService.logger = app.logger

# For testing in pycharm
# app.config.from_file(f"etc/user.toml", toml.load)
app.config.from_file(f"etc/{__name__}.toml", toml.load)
DBService.db_url = app.config["DATABASES"]["URL"]
DBService.db_path = app.config['DATABASES']["DB_PATH"]

dbService = DBService()

# The authentification response type
UNAUTHORIZED = {'WWW-Authenticate': 'Basic realm="Login Required"'}


# **************************************************************#
# **************************** User ****************************#
# **************************************************************#
# **************************************************************#
# **************************** User ****************************#
# **************************************************************#


@app.route('/auth')
async def auth():
    print(request)
    auth = request.authorization
    print(auth)
    if auth is not None and auth.type == "basic":
        username = auth.username
        password = auth.password
        print("Validating the username ", username, "and password ", password)
        if username is None or password is None:
            return quart.Response("Please log in. The username or password cannot be none", 401, UNAUTHORIZED)
        else:
            user = await find_user_by_name(username)
            if user is None:
                return quart.Response("Please log in. The username does not exist", 401, UNAUTHORIZED)
            else:
                if user.password == password:
                    msg = "Login success."
                    return {"authenticated": True}

                else:
                    return quart.Response("Please log in. Wrong username or password", 401, UNAUTHORIZED)
    else:
        # return 'WWW-Authenticate: Basic realm="My Realm" HTTP/1.0 401 Unauthorized'
        # This will prompt the user a dialog to enter username and password.
        return quart.Response("Please log in", 401, UNAUTHORIZED)

    return {"authenticated": True}


@app.route('/register', methods=["GET", "POST"])
async def register():
    if request.method == "GET":
        username = request.args.get('username')
        password = request.args.get('password')
    elif request.method == "POST":
        f = await request.form
        username = f.get('username')
        password = f.get('password')
    register_authenticated = False
    msg = ""
    try:
        if username is None or password is None:
            msg = "The username or password cannot be none"
            return {"msg": msg}, 401, {'X-Header': 'Value'}
        else:
            _id = await register(username, password)
            if _id is not None:
                if _id == 'existed':
                    msg = "The username is existed, please try another name."
                    return {"msg": msg}, 401, {'X-Header': 'Value'}
                else:
                    msg = "Success, you may try to login."
                    register_authenticated = True
    except Exception as e:
        print(e)
        print("System error, please contact the author.")
    return {"authenticated": register_authenticated, "msg": msg, "username": username}

    # ********************************** Find a user by username **********************************
    # noinspection PyUnreachableCode


async def find_user_by_name(name):
    # Insert sql statement
    sql = "select username, password from Users where username = '" + name + "'"
    app.logger.info(sql)
    row = await dbService.execute_sql_one(sql)
    # If ther user is not found, return ""
    if row is None:
        return None
    u = User(row[0], row[1])
    return u

    #


async def register(name, password):
    # If the user has existed, then refuse to register
    user = await find_user_by_name(name)
    if user is not None:
        return "existed"
    else:
        # Insert sql statement
        sql = "insert into Users(username, password) Values('" + name + "', '" + password + "')"
        return await dbService.insert(sql)


async def find_all_user():
    sql = 'select * from Users;'
    app.logger.info(sql)
    return await dbService.execute_sql_all(sql)


# @app.errorhandler(RequestSchemaValidationError)
def bad_request(e):
    return {"error": str(e.validation_error)}, 400


@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409


if __name__ == '__main__':
    try:
        DBService.app = app
        if DBService.db_url is None or DBService.db_path is None:
            print("The system initialization failed! Check the db address.")

        app.run(debug=True)
    except Exception as e:
        print(e)
        print("The system initialization failed, please contact the author.")
