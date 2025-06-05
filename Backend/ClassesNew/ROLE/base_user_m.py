from enum import UNIQUE

from peewee import *
import datetime

from Backend.data_base.core import BaseModel

class Role(BaseModel):
    id = AutoField()
    name = CharField(unique=True)
    access = BooleanField()

    INCOSATOR = 'incosator'
    BANK_WORKER = 'bankworker'
    USER = 'user'

class DefaultUser(BaseModel):
    role = ForeignKeyField(Role, backref='users', on_delete='CASCADE')
    id = AutoField()
    first_name = CharField()
    surname = CharField()
    last_name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

