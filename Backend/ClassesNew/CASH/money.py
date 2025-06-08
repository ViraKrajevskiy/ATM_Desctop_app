from peewee import *

from Backend.data_base.core import BaseModel

class Money(BaseModel):
    money_id = AutoField()
    money_nominal = IntegerField()
    types = CharField()
    date_made = DateTimeField()

