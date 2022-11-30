from service.DBServiceModule import DBService
import json
from view.ValidWords import ValidWords

class ValidWordsService(DBService):
    def __init__(self):
        super(ValidWordsService, self).__init__()


    async def import_from_json(self, list):
        # Insert sql statement
        n = 0
        for vd in list:

            sql = "insert into ValidWords(name, status) Values('" + vd.name + "', '" + str(vd.status) + "');"
            print(sql)
            _id = await self.insert(sql)
            vd.setId(_id)
            n+=1
        return list

    async def count_records(self):
        sql = "select count(*) from ValidWords;"
        row = await self.execute_sql_one(sql)
        count = row[0]
        return count

    async def import_correct_words(self):
        vws = ValidWordsService()
        list = []
        with open('json/correct.json', 'r') as f:
            data = json.load(f)
            for name in data:
                v = ValidWords(name, 1)  # Status 1 means secret word
                list.append(v)
        if list is not None:
            await vws.import_from_json(list)


    # ********************************** Already imported in database, check the db, don't insert repeatedly
    # **********************************

    async def import_valid_words(self):
        vws = ValidWordsService()
        list = []
        with open('json/valid.json', 'r') as f:
            data = json.load(f)
            for name in data:
                v = ValidWords(name, 0)  # Status 1 means secret word
                list.append(v)
        if list is not None:
            newList = await vws.import_from_json(list)
            print(len(newList))
