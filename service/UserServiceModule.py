from service.DBServiceModule import DBService
from view.User import User


# ********************************** User api, inheritance of DBService **********************************

class UserService(DBService):

    def __init__(self):
        super(UserService, self).__init__()

    # ********************************** Find a user by username **********************************
    async def find_user_by_name(self, name):
        # Insert sql statement
        sql = "select username, password from Users where username = '" + name + "'"
        row = await self.execute_sql_one(sql)
        # If ther user is not found, return ""
        if row is None:
            return None
        u = User(row[0], row[1])
        return u

    #
    async def register(self, name, password):
        # If the user has existed, then refuse to register
        user = await self.find_user_by_name(name)
        if user is not None:
            return "existed"
        else:
            # Insert sql statement
            sql = "insert into Users(username, password) Values('" + name + "', '" + password + "')"
            return await self.insert(sql)

    async def find_all_user(self):
        sql = 'select * from Users;'
        return await self.execute_sql_all(sql)
