from peewee import *
from Backend.data_base import BaseModel

class User(BaseModel):
    connect = ForeignKeyField(DefaultUser,)
