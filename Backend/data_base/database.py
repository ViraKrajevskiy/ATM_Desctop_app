from peewee import *

from Backend.ClassesNew.ROLE.base_user_m import DefaultUser

db = SqliteDatabase('DataBase.db')


class BaseModel(Model):
    class Meta:
        database = db

db.connect()
db.create_tables([DefaultUser])
db.create_tables([])
