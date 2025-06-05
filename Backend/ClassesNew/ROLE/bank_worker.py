from peewee import *

from Backend.ClassesNew.ROLE.base_user_m import Role, DefaultUser
from Backend.data_base.core import BaseModel

# class BankWorker(BaseModel):
#     login = CharField()
#     password = CharField()
#     enter = ManyToManyField(DefaultUser,backref='bankworker')
#
#
#     def save(self, *args, **kwargs):
#         role, created = Role.get_or_create(access=False, defaults={'id': None})
#         role_name = Role.BANK_WORKER
#         role_obj, _ = Role.get_or_create(id=2, defaults={'access': True})
#         self.enter.choicefl = role_obj
#         self.enter.save()
#         return super().save(*args, **kwargs)
#

class BankWorker(BaseModel):
    login = CharField()
    password = CharField()
    users = ManyToManyField(DefaultUser, backref='bankworkers')

    def save(self, *args, **kwargs):
        role_obj, _ = Role.get_or_create(name=Role.BANK_WORKER, defaults={'access': True})

        # Сохраняем самого работника
        super().save(*args, **kwargs)

        # Устанавливаем роль BANK_WORKER всем пользователям, связанным с этим работником
        for user in self.users:
            user.role = role_obj
            user.save()

        return self
        
