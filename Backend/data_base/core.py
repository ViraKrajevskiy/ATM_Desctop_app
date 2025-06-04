import os
from peewee import SqliteDatabase, Model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Путь к папке data_base
DB_PATH = os.path.join(BASE_DIR, 'DataBase.db')

# Создаем базу один раз с правильным путем
db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db
        