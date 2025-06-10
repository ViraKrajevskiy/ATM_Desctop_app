from peewee import *

from Backend.data_base.core import BaseModel


class Wallet(BaseModel):
    from Backend.ClassesNew.CASH.credit_cards import CreditCards
    id = AutoField()
    card = ForeignKeyField(CreditCards, backref='wallets')



class WalletMoney(BaseModel):
    from Backend.ClassesNew.CASH.money import Money
    wallet = ForeignKeyField(Wallet, backref='wallet_money')
    money = ForeignKeyField(Money, backref='wallet_money')
    quantity = IntegerField()  # Количество купюр данного номинала

    class Meta:
        indexes = (
            (('wallet', 'money'), True),  # уникальность пары кошелёк + номинал
        )


def add_bills(wallet_id: int, money_id: int, quantity_to_add: int):
    wallet_money, created = WalletMoney.get_or_create(wallet=wallet_id, money=money_id, defaults={'quantity': 0})
    wallet_money.quantity += quantity_to_add
    wallet_money.save()

# 💰 Получить общий баланс наличных в кошельке
def get_cash_balance(wallet_id: int):
    query = WalletMoney.select().where(WalletMoney.wallet_id == wallet_id)
    total = sum(entry.money.money_nominal * entry.quantity for entry in query)
    return total

