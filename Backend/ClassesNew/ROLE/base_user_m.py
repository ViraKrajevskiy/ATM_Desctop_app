from peewee import *
import datetime

from Backend.data_base.core import BaseModel

class Role(BaseModel):
    id = AutoField()
    name = CharField()
    access = BooleanField()

    INCOSATOR = 'incosator'
    BANK_WORKER = 'bankworker'
    USER = 'user'

class DefaultUser(BaseModel):
    choicefl = ManyToManyField(Role, backref='role')
    id = AutoField()
    first_name = CharField()
    surname = CharField()
    last_name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

