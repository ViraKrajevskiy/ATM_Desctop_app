from peewee import *

from Backend.data_base.core import BaseModel

class Money(BaseModel):
    moeny_id = AutoField()
    moeny_nominal = IntegerField()
    types = CharField()
    date_made = DateTimeField()

