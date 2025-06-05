import datetime
from Backend.data_base.core import db  # или как у тебя называется объект базы
from Backend.ClassesNew.ROLE.base_user_m import Role, DefaultUser
from Backend.ClassesNew.CASH.wallet import Wallet
from Backend.ClassesNew.CASH.credit_cards import CreditCards
from Backend.ClassesNew.CASH.money import Money, OtherRate
from Backend.ClassesNew.ATM.atm import Atm
from Backend.ClassesNew.ROLE.user import User
from Backend.ClassesNew.ROLE.bank_worker import BankWorker
from Backend.ClassesNew.ROLE.incasator import Incasator

def seed():
    db.connect()
    # Создаем таблицы (можно перечислить все нужные модели)
    db.create_tables([Role, DefaultUser, Wallet, CreditCards, Money, OtherRate, Atm, User, BankWorker, Incasator])
    db.close()

if __name__ == '__main__':
    seed()
    