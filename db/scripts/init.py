import os
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

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

if __name__ == '__main__':
    db = os.path.join('..', 'main.db')

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL,
                                age integer NOT NULL,
                                sex text NOT NULL,
                                email text NOT NULL,
                                phone text NOT NULL,
                                password text NOT NULL
                            ); """

    conn = create_connection(db)

    if conn is not None:
        create_table(conn, sql_create_users_table)
    else:
        print("Error! cannot create the database connection.")