from peewee import *


from Backend.data_base.core import BaseModel

class Atm(BaseModel):
    from Backend.ClassesNew.CASH.wallet import Wallet
    id = AutoField()
    location = CharField()
    wallet = ForeignKeyField(Wallet,backref='atms',on_delete='CASCADE')