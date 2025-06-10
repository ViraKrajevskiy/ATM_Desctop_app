from peewee import *


from Backend.data_base.core import BaseModel
from datetime import datetime
class Atm(BaseModel):
    from Backend.ClassesNew.CASH.wallet import WalletMoney

    id = AutoField()
    location = CharField()
    wallet = ForeignKeyField(WalletMoney,backref='atms',on_delete='CASCADE')


def transfer_cash_to_atm(user, atm, bills: dict[int, int], commission_rate=0.01):

    from Backend.ClassesNew.CASH.wallet import WalletMoney
    total_amount = 0

    for money_id, qty in bills.items():
        wm = WalletMoney.get(wallet=user.wallet, money=money_id)
        if wm.quantity < qty:
            raise ValueError(f"Недостаточно купюр номинала {wm.money.money_nominal}")
        wm.quantity -= qty
        wm.save()
        total_amount += qty * wm.money.money_nominal

    commission = int(total_amount * commission_rate)
    final_sum = total_amount - commission

    # Добавить деньги в кошелёк банкомата
    for money_id, qty in bills.items():
        atm_entry, _ = WalletMoney.get_or_create(wallet=atm.wallet, money=money_id, defaults={'quantity': 0})
        atm_entry.quantity += qty
        atm_entry.save()

    return {
        "Пользователь": user.username,
        "Сумма оплаты": total_amount,
        "Комиссия": commission,
        "Итого переведено банкомату": final_sum,
        "Время": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }



