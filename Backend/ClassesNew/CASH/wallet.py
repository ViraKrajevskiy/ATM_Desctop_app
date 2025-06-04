from peewee import *

from Backend.data_base.core import BaseModel


class Wallet(BaseModel):
    id = AutoField()
    from Backend.ClassesNew.CASH.credit_cards import CreditCards
    from Backend.ClassesNew.CASH.money import Money,OtherRate
    money_count = ForeignKeyField(Money, backref='money')
    other_money = ForeignKeyField(OtherRate, backref='otherrate')
    card = ForeignKeyField(CreditCards, backref='card')

    def get_wallet_balance(wallet_id: int):
        wallet = Wallet.get_by_id(wallet_id)
        total = 0
        for money in wallet.money:  # .money — через backref
            total += money.nominal.value * money.count
        return total
