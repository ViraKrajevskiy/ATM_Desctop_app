from peewee import *
from Backend.ClassesNew.ROLE.base_user_m import Role, DefaultUser
from Backend.data_base.core import BaseModel
from Backend.ClassesNew.CASH.wallet import Wallet

class User(BaseModel):
    connect = ForeignKeyField(DefaultUser,backref='user')
    wallet = ManyToManyField(Wallet, backref='users')

    def save(self, *args, **kwargs):
        role_obj, _ = Role.get_or_create(id=2, defaults={'access': True})
        self.connect.choicefl = role_obj
        self.connect.save()
        return super().save(*args, **kwargs)
        