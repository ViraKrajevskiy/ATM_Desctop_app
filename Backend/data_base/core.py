from peewee import SqliteDatabase, Model

db = SqliteDatabase('DataBase.db')

class BaseModel(Model):
    class Meta:
        database = db
        