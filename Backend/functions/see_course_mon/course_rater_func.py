from Backend.data_base import BaseModel,db
from peewee import *
import random
import threading
import time
from datetime import datetime,timezone

import os

print(os.getcwd())
class CurrencyRate(BaseModel):
    id = AutoField()
    currency_pair = CharField()
    rate = FloatField()
    timestamp = DateTimeField(default=datetime.utcnow)


#  Функция обновления курса
def update_currency_rate(currency_pair: str, min_rate: float, max_rate: float):
    while True:
        new_rate = round(random.uniform(min_rate, max_rate), 2)
        now = datetime.now(timezone.utc)

        CurrencyRate.create(
            currency_pair=currency_pair,
            rate=new_rate,
            timestamp=now
        )

        print(f"[{now}] {currency_pair} -> {new_rate}")

        # Оставляем только 10 последних записей, удаляем остальные
        rates = (CurrencyRate
                 .select()
                 .where(CurrencyRate.currency_pair == currency_pair)
                 .order_by(CurrencyRate.timestamp.desc()))
        if rates.count() > 10:
            # Получаем записи, которые надо удалить (старее 10 последних)
            to_delete = rates.offset(10)
            ids_to_delete = [rate.id for rate in to_delete]
            CurrencyRate.delete().where(CurrencyRate.id.in_(ids_to_delete)).execute()

        time.sleep(240)
# 2 минуты

# Запуск потоков симуляции
def start_currency_simulation():
    currency_pairs = {
        "SUM->USD": (12500, 13300),
        "SUM->RUB": (120, 140),
        "SUM->EUR": (12500, 13500),
    }

    for pair, (min_r, max_r) in currency_pairs.items():
        threading.Thread(target=update_currency_rate, args=(pair, min_r, max_r), daemon=True).start()


#  Просмотр всех записей (по желанию)
def print_all_records():
    print("--- CurrencyRate ---")
    for rate in CurrencyRate.select():
        print(rate.__data__)
    print()


if __name__ == "__main__":
    if db.is_closed():
        db.connect()

    start_currency_simulation()  # запускаем потоки симуляции

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Симуляция остановлена.")
        db.close()
        