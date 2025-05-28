from peewee import *
import datetime

from Backend.data_base.database import BaseModel

class Role(BaseModel):
    id = AutoField()
    name =  CharField()
    access = BooleanField(default=False)

class BaseUser(BaseModel):
    role_id = ForeignKeyField(Role, related_name='users')
    id = AutoField()
    first_name = CharField()
    surname = CharField()
    last_name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)