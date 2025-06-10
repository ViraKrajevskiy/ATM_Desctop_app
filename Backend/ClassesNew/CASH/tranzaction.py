from peewee import *
from Backend.data_base import BaseModel

class TranzactionMoney(BaseModel):
    from Backend.ClassesNew.ATM.atm import Atm
    from Backend.ClassesNew.ROLE.user import User

    money = AutoField()
    payment_type = CharField()
    pay_in = ForeignKeyField(Atm, backref='do_these_bacnomat')  # Аналогично стоит проверить этот
    User = ForeignKeyField(User, backref='whopayed')
