from peewee import *

from Backend.ClassesNew.ROLE.base_user_m import Role, DefaultUser
from Backend.data_base.core import BaseModel

class BankWorker(BaseModel):
    login = CharField()
    password = CharField()
    user = ForeignKeyField(DefaultUser, backref='bank_worker', null=False)  # Must have a user

    def save(self, *args, **kwargs):
        # Ensure the user has the correct role
        if not self.user.role or self.user.role.name != Role.BANK_WORKER:
            role = Role.get_or_create(name=Role.BANK_WORKER, defaults={'access': True})[0]
            self.user.role = role
            self.user.save()
        return super().save(*args, **kwargs)
        
