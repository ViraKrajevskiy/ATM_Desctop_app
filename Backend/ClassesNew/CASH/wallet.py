from peewee import *

from Backend.data_base.core import BaseModel


class Wallet(BaseModel):
    from Backend.ClassesNew.CASH.credit_cards import CreditCards
    from Backend.ClassesNew.CASH.money import Money
    id = AutoField()
    money = ForeignKeyField(Money, backref='wallets')
    card = ForeignKeyField(CreditCards, backref='wallets')

    def get_wallet_balance(wallet_id: int):
        wallet = Wallet.get_by_id(wallet_id)
        total = 0
        for money in wallet.money:  # .money — через backref
            total += money.nominal.value * money.count
        return total
