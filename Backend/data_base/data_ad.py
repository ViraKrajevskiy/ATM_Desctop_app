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

    # Заполняем таблицу Role начальными данными
    Role.insert_many([
        {'id': 1, 'name': 'incosator', 'access': True},
        {'id': 2, 'name': 'user', 'access': True},
        {'id': 3, 'name': 'bankworker', 'access': True},
    ]).execute()

    # Добавляем DefaultUser
    DefaultUser.insert_many([
        {'id': 1, 'first_name': 'Иван', 'surname': 'Иванов', 'last_name': 'Иванович', 'created_at': datetime.datetime.now()},
        {'id': 2, 'first_name': 'Пётр', 'surname': 'Петров', 'last_name': 'Петрович', 'created_at': datetime.datetime.now()},
    ]).execute()

    # Пример создания Wallet, Money, CreditCards и связывания
    money1 = Money.create(moeny_nominal=100, type='RUB', date_made=datetime.datetime.now())
    money2 = Money.create(moeny_nominal=50, type='RUB', date_made=datetime.datetime.now())
    other_rate = OtherRate.create(moeny_nominal=10, type='USD', date_made=datetime.datetime.now())
    card = CreditCards.create(card_number=1234567890123456, balance=5000, security_code=123,
                              special_identificator='XYZ123', bank_name='MyBank', card_type='Visa',
                              card_give_date=datetime.datetime.now(), card_end_date=datetime.datetime(2030,1,1))

    wallet = Wallet.create(money_count=money1, other_money=other_rate, card=card)

    # Можно создавать пользователей и связывать с кошельками и ролями
    user_default = DefaultUser.get_by_id(1)
    user_default.choicefl.add(Role.get(Role.id == 2))  # добавляем роль user

    user = User.create(connect=user_default)
    user.wallet.add(wallet)

    db.close()

if __name__ == '__main__':
    seed()
    