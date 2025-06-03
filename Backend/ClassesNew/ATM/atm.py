from peewee import *

from Backend.ClassesNew.CASH.wallet import Wallet
from Backend.data_base.core import BaseModel

class Atm(BaseModel):
    id = AutoField()
    location = CharField()
    Money = ForeignKeyField(Wallet,backref='eusde')