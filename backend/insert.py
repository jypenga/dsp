import os
import sqlite3

from sqlite3 import Error
from .connect import with_connection

# PATH specified for calls from app.py
PATH = os.path.join('db', 'main.db')

@with_connection(db=PATH)
def insert_log(conn, id, args):
    sql = """INSERT INTO logs (patient, title, extra, day, month, year)
             VALUES
             (?, ?, ?, ?, ?, ?);"""
    retcode = 0
    try:
        c = conn.cursor()
        c.execute(sql, (id, *args))
        retcode = 1
    except Error as e:
        print(e)
    return retcode

@with_connection(db=PATH)
def insert_patient(conn, id, args):
    sql = """INSERT INTO patients (user, name, age, sex, height, weight)
             VALUES
             (?, ?, ?, ?, ?, ?);"""
    retcode = 0
    try:
        c = conn.cursor()
        c.execute(sql, (id, *args))
        retcode = 1
    except Error as e:
        print(e)
    return retcode

@with_connection(db=PATH)
def insert_medication(conn, id, args):
    sql = """INSERT INTO medication (patient, name, type, time_range, time_start, time_end, meal, specific, reason)
             VALUES
             (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    retcode = 0
    try:
        c = conn.cursor()
        c.execute(sql, (id, *args))
        retcode = 1
    except Error as e:
        print(e)
    return retcode