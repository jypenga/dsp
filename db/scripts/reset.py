import os
from re import A
import sys
import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def delete_all(conn, delete_all_sql):
    try:
        c = conn.cursor()
        c.execute(delete_all_sql)
    except Error as e:
        print(e)

if __name__ == '__main__':
    db = os.path.join('..', 'main.db')

    sql_delete_users = """DROP TABLE users;"""
    sql_delete_patients = """DROP TABLE patients;"""
    sql_delete_medication = """DROP TABLE medication;"""
    sql_delete_diet = """DROP TABLE diet;"""
    sql_delete_logs = """DROP TABLE logs;"""

    conn = create_connection(db)

    perm = input('Do you really wish to reset the database? All data will be lost. [y/n]\n')
    if perm == 'y':
        if conn is not None:
            delete_all(conn, sql_delete_users)
            delete_all(conn, sql_delete_patients)
            delete_all(conn, sql_delete_medication)
            delete_all(conn, sql_delete_diet)
            delete_all(conn, sql_delete_logs)
        else:
            print("Error! cannot create the database connection.")
        print('Database succesfully reset.')
    else:
        print('Reset cancelled.')
        sys.exit()