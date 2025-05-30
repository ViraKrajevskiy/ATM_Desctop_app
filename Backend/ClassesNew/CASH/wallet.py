from peewee import *

from Backend.data_base.database import BaseModel


class Wallet(BaseModel):
    id = AutoField()
    money_count = [IntegerField(),]
    card = ForeignKeyField('Card', backref='card')
