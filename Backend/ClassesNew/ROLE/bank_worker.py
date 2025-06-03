from peewee import *

from Backend.ClassesNew.ROLE.base_user_m import Role, DefaultUser
from Backend.data_base.core import BaseModel

class BankWorker(BaseModel):
    login = CharField(unique=True)
    password = CharField(unique=True)
    enter = ManyToManyField(DefaultUser,backref='bankworker')


    def save(self, *args, **kwargs):
        role, created = Role.get_or_create(access=False, defaults={'id': None})
        role_name = Role.BANK_WORKER
        role_obj, _ = Role.get_or_create(id=3, defaults={'access': True})
        self.enter.choicefl = role_obj
        self.enter.save()
        return super().save(*args, **kwargs)


