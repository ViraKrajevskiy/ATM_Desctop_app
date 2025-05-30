from itertools import count
from peewee import *

from Backend.ClassesNew.CASH.credit_cards import CreditCards
from Backend.ClassesNew.CASH.money import Money
from Backend.data_base.core import BaseModel

class Atm(BaseModel):
    id = AutoField()
    location = CharField()
    card = ForeignKeyField(CreditCards, backref='card')
    balance_money = ForeignKeyField(Money, backref='balance_money')





