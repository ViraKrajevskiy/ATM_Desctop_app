from peewee import *
from Backend.ClassesNew.ROLE.base_user_m import Role, DefaultUser
from Backend.data_base.core import BaseModel
from Backend.ClassesNew.CASH.wallet import Wallet

class User(BaseModel):
    connect = ForeignKeyField(DefaultUser, backref='user_profile')
    wallet = ManyToManyField(Wallet, backref='users')

    def save(self, *args, **kwargs):
        # Убедимся, что у пользователя есть роль USER
        if not hasattr(self.connect, 'role') or self.connect.role.name != Role.USER:
            role, _ = Role.get_or_create(
                name=Role.USER,
                defaults={'access': True}
            )
            self.connect.role = role
            self.connect.save()
        return super().save(*args, **kwargs)

# Промежуточная таблица для связи ManyToMany
UserWalletThrough = User.wallet.get_through_model()