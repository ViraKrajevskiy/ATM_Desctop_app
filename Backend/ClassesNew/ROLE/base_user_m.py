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

    @classmethod
    def create_default_roles(cls):
        roles = [
            (cls.INCOSATOR, True),
            (cls.BANK_WORKER, True),
            (cls.USER, False),
        ]
        for role_name, access in roles:
            if not cls.select().where(cls.name == role_name).exists():
                cls.create(name=role_name, access=access)

                
class DefaultUser(BaseModel):
    role = ForeignKeyField(Role, backref='users', on_delete='CASCADE')
    id = AutoField()
    first_name = CharField()
    surname = CharField()
    last_name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

