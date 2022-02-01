import os
import sqlite3

import numpy as np

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

@with_connection(db=PATH)
def get_patients(conn, id):
    sql = """SELECT * FROM patients WHERE user=?;"""
    ret = []
    if not id:
        return ret
    try:
        c = conn.cursor()
        c.execute(sql, (id))
        ret = c.fetchall()
    except Error as e:
        print(e)
    return ret

@with_connection(db=PATH)
def get_patient(conn, id):
    sql = """SELECT * FROM patients WHERE id=?;"""
    ret = []
    if not id:
        return ret
    try:
        c = conn.cursor()
        c.execute(sql, (id))
        ret = c.fetchall()[0]
    except Error as e:
        print(e)
    return ret

@with_connection(db=PATH)
def get_patient_medication(conn, id):
    sql = """SELECT * FROM medication WHERE patient=? ORDER BY id ASC;"""
    ret = []
    if not id:
        return ret
    try:
        c = conn.cursor()
        c.execute(sql, (id))
        ret = c.fetchall()
    except Error as e:
        print(e)
    return ret

@with_connection(db=PATH)
def get_patient_diet(conn, id):
    sql = """SELECT * FROM diet WHERE patient=?;"""
    ret = []
    if not id:
        return ret
    try:
        c = conn.cursor()
        c.execute(sql, (id))
        ret = c.fetchall()[0]
    except Error as e:
        print(e)
    return ret

@with_connection(db=PATH)
def get_patient_logs(conn, id):
    sql = """SELECT * FROM logs WHERE patient=? ORDER BY day DESC;"""
    ret = []
    if not id:
        return ret
    try:
        c = conn.cursor()
        c.execute(sql, (id))
        ret = c.fetchall()
    except Error as e:
        print(e)
    return ret

@with_connection(db=PATH)
def get_patient_score(conn, id):
    sql = """SELECT score FROM data WHERE patient=? ORDER BY id DESC;"""
    ret = []
    if not id:
        return ret
    try:
        c = conn.cursor()
        c.execute(sql, (id, ))
        ret = c.fetchall()
        if len(ret) > 0:
            ret = ret[0][0]
        else:
            ret = 3
    except Error as e:
        print(e)
    return ret