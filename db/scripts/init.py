import os
import bcrypt
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

def do(conn, sql, *args):
    try:
        c = conn.cursor()
        c.execute(sql, (*args,))
        conn.commit()
    except Error as e:
        print(e)

if __name__ == '__main__':
    db = os.path.join('..', 'main.db')

    # create tables
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL,
                                age integer NOT NULL,
                                sex text NOT NULL,
                                email text NOT NULL,
                                phone text NOT NULL,
                                password text NOT NULL); """

    sql_create_patients_table = """CREATE TABLE IF NOT EXISTS patients (
                                   id integer PRIMARY KEY AUTOINCREMENT,
                                   user integer NOT NULL,
                                   name text NOT NULL,
                                   age integer NOT NULL,
                                   sex text NOT NULL,
                                   height real NOT NULL,
                                   weight real NOT NULL,
                                   avatar text NOT NULL,
                                   score real NOT NULL,
                                   doctor text,
                                   doctor_phone text,
                                   provider text,
                                   background text); """

    sql_create_medication_table = """"""

    sql_create_log_table = """CREATE TABLE IF NOT EXISTS logs (
                              id integer PRIMARY KEY AUTOINCREMENT,
                              patient integer NOT NULL,
                              title text NOT NULL,
                              date text NOT NULL,
                              health integer NOT NULL,
                              mood NOT NULL,
                              extra text); """

    # create dummy entries
    sql_insert_dummy_users = """INSERT INTO users (name, age, sex, email, phone, password)
                             VALUES
                             ("Admin Admin", 99, "a", "admin@monizorg.nl", "1234", ?),
                             ("Boris Boef", 13, "m", "bboef@duckstad.nl", "1234", ?);"""

    sql_insert_dummy_patients = """INSERT INTO patients (user, name, age, sex, height, weight, avatar, score)
                                VALUES
                                (1, "Harry Houdini", 63, "m", 1.80, 80.8, "avatar-m.png", 0),
                                (1, "Ritish Changoer", 1, "m", 1.60, 200.1, "avatar-m.png", 0),
                                (1, "Taylor Swift", 40, "v", 1.80, 55.3, "avatar-f.png", 0),
                                (2, "Kevin Kevin", 55, "m", 1.50, 70.8, "avatar-f.png", 0),
                                (2, "Chris Evans", 1, "m", 1.80, 90.6, "avatar-m.png", 0),
                                (2, "Anouk Hooijschuur", 2, "v", 1.70, "avatar-f.png", 60.4, 0),
                                (2, "Vera Verbanescu", 42, "v", 1.76, "avatar-f.png", 70.9, 0);"""

    sql_insert_dummy_logs = """INSERT INTO logs (patient, title, date, health, mood, extra)
                             VALUES
                             (2, "RITISH!", "17-01-2022", 3, 3, "Ritish voelt zich alweer erg goed."),
                             (2, "ritish", "16-01-2022", 3, 3, "Ritish voelt zich goed.");"""

    conn = create_connection(db)

    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_patients_table)
        create_table(conn, sql_create_log_table)

        hashed_pw_1 = bcrypt.hashpw(bytes('admin', encoding='utf-8'), bcrypt.gensalt())
        hashed_pw_2 = bcrypt.hashpw(bytes('abc', encoding='utf-8'), bcrypt.gensalt())

        do(conn, sql_insert_dummy_users, hashed_pw_1, hashed_pw_2)
        do(conn, sql_insert_dummy_patients)
        do(conn, sql_insert_dummy_logs)
    else:
        print("Error! cannot create the database connection.")

    conn.close()