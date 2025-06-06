def create_all_tables():
    from Backend.ClassesNew.CASH.credit_cards import CreditCards, PhoneNumber
    from Backend.ClassesNew.CASH.money import Money
    from Backend.ClassesNew.CASH.tranzaction import TranzactionMoney
    from Backend.ClassesNew.CASH.wallet import Wallet
    from Backend.ClassesNew.ROLE.bank_worker import BankWorker
    from Backend.ClassesNew.ROLE.base_user_m import DefaultUser,Role
    from Backend.ClassesNew.ROLE.incasator import Incasator
    from Backend.data_base.core import db
    from Backend.ClassesNew.ROLE.user import User

    from Backend.ClassesNew.ATM.atm import Atm
    from Backend.functions.see_course_mon.course_rater_func import CurrencyRate
    db.create_tables([
        Role, DefaultUser, User,
        Incasator, BankWorker,
        Money, PhoneNumber, CreditCards,
        Wallet, Atm, CurrencyRate,TranzactionMoney,CreditCards.phone_field.get_through_model()
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
    from Backend.ClassesNew.ROLE.base_user_m import DefaultUser,Role
    from Backend.ClassesNew.ROLE.incasator import Incasator
    from Backend.ClassesNew.ROLE.user import User

    from Backend.ClassesNew.ATM.atm import Atm
    from Backend.functions.see_course_mon.course_rater_func import CurrencyRate
    
    models = [
        CreditCards.phone_field.get_through_model(),
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


if __name__ == "__main__":
    main()