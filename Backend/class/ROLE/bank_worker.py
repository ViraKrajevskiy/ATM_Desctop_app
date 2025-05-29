from peewee import ForeignKeyField

from Backend.data_base import BaseModel

class BankWorker(BaseModel):
    enter = ForeignKeyField(BaseUser,)