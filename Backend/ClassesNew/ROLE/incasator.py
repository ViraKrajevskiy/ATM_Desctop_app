from peewee import *

from Backend.ClassesNew.CASH.wallet import Wallet
from Backend.ClassesNew.ROLE.base_user_m import DefaultUser, Role
from Backend.data_base.core import BaseModel


class Incasator(BaseModel):
    login = CharField()
    password = CharField()
    default_user = ForeignKeyField(DefaultUser, related_name='incasator')
    wallet = ManyToManyField(Wallet,backref='moen')

    def save(self, *args, **kwargs):
        role_obj, _ = Role.get_or_create(id=1, defaults={'access': True})
        self.default_user.choicefl = role_obj
        self.default_user.save()
        return super().save(*args, **kwargs)