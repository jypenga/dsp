import os
import sqlite3

from sqlite3 import Error
from .connect import with_connection

# PATH specified for calls from app.py
PATH = os.path.join('db', 'main.db')

@with_connection(db=PATH)
def init_register(conn, name, age, sex, email, tel, pw):
    sql = """INSERT INTO users (name, age, sex, email, phone, password)
    VALUES(?, ?, ?, ?, ?, ?);"""
    try:
        c = conn.cursor()
        c.execute(sql, (name, age, sex, email, tel, pw))
    except Error as e:
        print(e)
    return