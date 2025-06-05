from peewee import *

from Backend.ClassesNew.CASH.wallet import Wallet
from Backend.ClassesNew.ROLE.base_user_m import DefaultUser, Role
from Backend.data_base.core import BaseModel


class Incasator(BaseModel):
    login = CharField()
    password = CharField()
    default_user = ForeignKeyField(DefaultUser, backref='incasator')
    # ManyToMany через Wallet
    wallet = ManyToManyField(Wallet, backref='incasators')

    def save(self, *args, **kwargs):
        role_obj, _ = Role.get_or_create(id=1, defaults={'name': Role.INCOSATOR, 'access': True})
        self.default_user.role = role_obj
        self.default_user.save()
        return super().save(*args, **kwargs)
        
# Промежуточная таблица для M2M
IncasatorWallet = Incasator.wallet.get_through_model()
