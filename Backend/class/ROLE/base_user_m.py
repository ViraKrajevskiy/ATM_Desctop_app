from peewee import *
import datetime

from Backend.data_base.database import BaseModel

class Role(BaseModel):
    id = AutoField()
    INCOSATOR = 'Incosator'
    BANK_WORKER = 'BankWorker'
    USER = 'User'
    access = BooleanField(default=False)

class DefaultUser(BaseModel):
    choicefl = ()
    id = AutoField()
    first_name = CharField()
    surname = CharField()
    last_name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)