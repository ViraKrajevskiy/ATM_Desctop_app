from peewee import *

db = SqliteDatabase('DataBase.db')


class BaseModel(Model):
    class Meta:
        database = db

db.connect()
db.create_tables([BaseUser])
db.create_tables([])
