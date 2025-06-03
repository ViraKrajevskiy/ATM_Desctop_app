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

        # Добавление новой записи
        CurrencyRate.create(
            currency_pair=currency_pair,
            rate=new_rate,
            timestamp=now
        )

        print(f"[{now}] {currency_pair} -> {new_rate}")

        # Удаление старых записей, оставляя только 10 последних
        query = (CurrencyRate
                 .select()
                 .where(CurrencyRate.currency_pair == currency_pair)
                 .order_by(CurrencyRate.timestamp.desc()))

        if query.count() > 10:
            for old_record in query[10:]:
                old_record.delete_instance()

        time.sleep(120)  # 2 минуты

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


# Главная точка входа
if __name__ == "__main__":
    if db.is_closed():
        db.connect()

    db.create_tables([CurrencyRate])
    start_currency_simulation()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Симуляция остановлена.")
        db.close()
