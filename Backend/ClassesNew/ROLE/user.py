from peewee import *

from Backend.ClassesNew.ROLE.base_user_m import Role, DefaultUser
from Backend.data_base.core import BaseModel


class User(BaseModel):
    connect = ForeignKeyField(DefaultUser,backref='user')
    
    def save(self, *args, **kwargs):
        role_obj, _ = Role.get_or_create(id=2, defaults={'access': True})
        self.connect.choicefl = role_obj
        self.connect.save()
        return super().save(*args, **kwargs)