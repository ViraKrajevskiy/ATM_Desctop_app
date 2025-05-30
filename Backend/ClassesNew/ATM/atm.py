from itertools import count

from peewee import *

from Backend.data_base.database import BaseModel

class Atm(BaseModel):
    id = AutoField()
    location = CharField()
    card = ForeignKeyField('Card', backref='card')
    balance_money = ForeignKeyField('Money', backref='balance_money')

    def count_money(self):
        pass