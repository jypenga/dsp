import os
import sqlite3

from sqlite3 import Error
from .connect import with_connection

# PATH specified for calls from app.py
PATH = os.path.join('db', 'main.db')

@with_connection(db=PATH)
def get_name(conn, id):
    sql = """SELECT name FROM users WHERE id=?;"""
    ret = None
    try:
        c = conn.cursor()
        c.execute(sql, (id))
        ret = c.fetchall()[0]
    except Error as e:
        print(e)
    return ret