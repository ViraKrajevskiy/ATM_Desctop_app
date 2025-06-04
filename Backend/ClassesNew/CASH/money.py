from peewee import *

from Backend.data_base.core import BaseModel

class Money(BaseModel):
    moeny_id = AutoField()
    moeny_nominal = IntegerField()
    type = CharField()
    date_made = DateTimeField()

class OtherRate(BaseModel):
    moeny_ids = AutoField()
    moeny_nominal = IntegerField()
    type = CharField()
    date_made = DateTimeField()
