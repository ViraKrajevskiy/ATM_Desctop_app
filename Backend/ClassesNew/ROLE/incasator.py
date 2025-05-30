from enum import UNIQUE

from peewee import *

from Backend.ClassesNew.ROLE.base_user_m import DefaultUser, Role
from Backend.data_base.database import BaseModel


class Incasator(BaseModel):
    login = CharField(UNIQUE=True)
    password = CharField(UNIQUE=True)
    default_user = ForeignKeyField('DefaultUser', related_name='incasator')

    def save(self, *args, **kwargs):
        role_obj, _ = Role.get_or_create(id=1, defaults={'access': True})
        self.default_user.choicefl = role_obj
        self.default_user.save()
        return super().save(*args, **kwargs)