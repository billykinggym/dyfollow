import os

from peewee import SqliteDatabase

os.makedirs('data', exist_ok=True)
db = SqliteDatabase('data/douyin.db')