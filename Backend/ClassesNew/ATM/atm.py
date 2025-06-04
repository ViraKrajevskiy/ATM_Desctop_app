from peewee import *


from Backend.data_base.core import BaseModel

class Atm(BaseModel):
    from Backend.ClassesNew.CASH.wallet import Wallet
    id = AutoField()
    location = CharField()
    Money = ManyToManyField(Wallet,backref='eusde')