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

    sql_create_medication_table = """CREATE TABLE IF NOT EXISTS medication (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                patient integer NOT NULL,
                                name text NOT NULL,
                                type text NOT NULL,
                                time_range integer NOT NULL,
                                time_start text NOT NULL,
                                time_end text NOT NULL,
                                meal integer NOT NULL,
                                specific integer NOT NULL,
                                reason text); """

    sql_create_diet_table = """CREATE TABLE IF NOT EXISTS diet (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                patient integer NOT NULL,
                                breakfast integer NOT NULL,
                                breakfast_start text,
                                breakfast_end text,
                                lunch integer NOT NULL,
                                lunch_start text,
                                lunch_end text,
                                dinner integer NOT NULL,
                                dinner_start text,
                                dinner_end text,
                                vegetarian integer,
                                vegan integer,
                                allergies text,
                                extra text); """

    sql_create_log_table = """CREATE TABLE IF NOT EXISTS logs (
                              id integer PRIMARY KEY AUTOINCREMENT,
                              patient integer NOT NULL,
                              title text NOT NULL,
                              day integer NOT NULL,
                              month integer NOT NULL,
                              year integer NOT NULL,
                              health integer,
                              mood integer,
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

    sql_insert_dummy_logs = """INSERT INTO logs (patient, title, day, month, year, health, mood, extra)
                             VALUES
                             (2, "RITISH!", 17, 1, 2022, 3, 3, "Ritish voelt zich alweer erg goed."),
                             (2, "ritish", 16, 1, 2022, 3, 3, "Ritish voelt zich goed.");"""

    sql_insert_dummy_medication = """INSERT INTO medication (patient, name, type, time_range, time_start, time_end, meal, specific, reason)
                             VALUES
                             (2, "XTC", "Pillen", 1, "23:00", "24:00", 3, 3, "Lekker genieten."),
                             (2, "Insuline", "Injectie", 1, "8:00", "9:00", 1, 1, "Noodzaak.");"""

    sql_insert_dummy_diet = """INSERT INTO diet (patient, breakfast, breakfast_start, breakfast_end, lunch, dinner, dinner_start, dinner_end, vegetarian, allergies, extra)
                             VALUES
                             (2, 1, "8:00", "9:00", 0, 1, "18:00", "19:00", 1, "Pinda's", "Houdt niet van andijvie.");"""

    conn = create_connection(db)

    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_patients_table)
        create_table(conn, sql_create_medication_table)
        create_table(conn, sql_create_diet_table)
        create_table(conn, sql_create_log_table)

        hashed_pw_1 = bcrypt.hashpw(bytes('admin', encoding='utf-8'), bcrypt.gensalt())
        hashed_pw_2 = bcrypt.hashpw(bytes('abc', encoding='utf-8'), bcrypt.gensalt())

        do(conn, sql_insert_dummy_users, hashed_pw_1, hashed_pw_2)
        do(conn, sql_insert_dummy_patients)
        do(conn, sql_insert_dummy_medication)
        do(conn, sql_insert_dummy_diet)
        do(conn, sql_insert_dummy_logs)
    else:
        print("Error! cannot create the database connection.")

    conn.close()