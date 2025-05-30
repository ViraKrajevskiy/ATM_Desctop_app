from peewee import *
import datetime

from Backend.ClassesNew.ROLE.user import User
from Backend.data_base.core import BaseModel


class PhoneNumber(BaseModel):
    id = AutoField()
    balance = IntegerField()
    phone_number = CharField()

class CreditCards(BaseModel):
    id = AutoField()

    owner = ForeignKeyField(User, backref='owner')

    card_number = IntegerField()
    balance = IntegerField()
    security_code = IntegerField()
    special_identificator = CharField()

    bank_name = CharField()
    card_type = CharField(max_length=50)

    card_give_date = DateField(default=datetime.datetime.now)
    card_end_date = DateField()
    phone_field = ForeignKeyField(PhoneNumber, backref='phones')