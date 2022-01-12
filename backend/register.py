import os
import sqlite3

from sqlite3 import Error
from .connect import with_connection

# PATH specified for calls from app.py
PATH = os.path.join('db', 'main.db')

@with_connection(db=PATH)
def init_register(conn, name):
    sql = """INSERT INTO users (name)
             VALUES(%s)""" % name
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

    return