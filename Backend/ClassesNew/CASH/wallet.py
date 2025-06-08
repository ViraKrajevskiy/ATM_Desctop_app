from peewee import *

from Backend.data_base.core import BaseModel


class Wallet(BaseModel):
    from Backend.ClassesNew.CASH.credit_cards import CreditCards
    from Backend.ClassesNew.CASH.money import Money
    id = AutoField()
    money = ForeignKeyField(Money, backref='wallets')
    card = ForeignKeyField(CreditCards, backref='wallets')

    @staticmethod
    def get_card_balance(card_id: int):
        query = Wallet.select().where(Wallet.card_id == card_id)
        total = sum(w.money.money_nominal for w in query)
        return total
