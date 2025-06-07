def create_all_tables():
    from Backend.ClassesNew.CASH.credit_cards import CreditCards, PhoneNumber
    from Backend.ClassesNew.CASH.money import Money
    from Backend.ClassesNew.CASH.tranzaction import TranzactionMoney
    from Backend.ClassesNew.CASH.wallet import Wallet
    from Backend.ClassesNew.ROLE.bank_worker import BankWorker
    from Backend.ClassesNew.ROLE.base_user_m import DefaultUser, Role
    from Backend.ClassesNew.ROLE.incasator import Incasator
    from Backend.ClassesNew.ROLE.user import User


    from Backend.data_base.core import db
    from Backend.ClassesNew.ATM.atm import Atm
    from Backend.functions.see_course_mon.course_rater_func import CurrencyRate

    # Получаем промежуточные таблицы ManyToMany
    creditcard_phone_through = CreditCards.phone_field.get_through_model()
    user_wallet_through = User.wallet.get_through_model()

    db.create_tables([
        Role, DefaultUser, User,
        Incasator, BankWorker,
        Money, PhoneNumber, CreditCards,
        Wallet, Atm, CurrencyRate, TranzactionMoney,
        creditcard_phone_through,
        user_wallet_through,  # <-- обязательно добавить эту таблицу
    ])


def print_all_records(model):
    print(f"--- {model.__name__} ---")
    for obj in model.select():
        print(obj.__data__)
    print()

def main():
    create_all_tables()
    from Backend.ClassesNew.CASH.credit_cards import CreditCards, PhoneNumber
    from Backend.ClassesNew.CASH.money import Money
    from Backend.ClassesNew.CASH.tranzaction import TranzactionMoney
    from Backend.ClassesNew.CASH.wallet import Wallet
    from Backend.ClassesNew.ROLE.bank_worker import BankWorker
    from Backend.ClassesNew.ROLE.base_user_m import DefaultUser, Role
    from Backend.ClassesNew.ROLE.incasator import Incasator
    from Backend.ClassesNew.ROLE.user import User

    from Backend.ClassesNew.ATM.atm import Atm
    from Backend.functions.see_course_mon.course_rater_func import CurrencyRate

    creditcard_phone_through = CreditCards.phone_field.get_through_model()
    user_wallet_through = User.wallet.get_through_model()

    models = [
        creditcard_phone_through,
        user_wallet_through,  # <-- добавить
        PhoneNumber,
        CreditCards,
        BankWorker,
        User,
        Incasator,
        DefaultUser,
        Role,
        Money,
        Wallet,
        Atm,
        CurrencyRate,
        TranzactionMoney
    ]
    for model in models:
        print_all_records(model)

    Role.create_default_roles()
    



if __name__ == "__main__":
    main()