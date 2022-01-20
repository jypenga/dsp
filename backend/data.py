import pandas as pd
import numpy as np
import datetime as dt

from datetime import datetime

import os

heart_rate = pd.read_csv(os.path.join('..', 'Data', 'heartrate_seconds_merged.csv')) #, nrows=100000)
heart_rate.Time = heart_rate.Time.apply(lambda s: datetime.strptime(s, '%m/%d/%Y %I:%M:%S %p'))

# only select heart rates between 07:00 and 22:00
heart_rate = heart_rate.iloc[pd.DatetimeIndex(heart_rate['Time']).indexer_between_time('7:00','22:00')]

heart_rate['jaar'] = heart_rate.Time.dt.year
heart_rate['maand'] = heart_rate.Time.dt.month
heart_rate['dag'] = heart_rate.Time.dt.day
heart_rate['uur'] = heart_rate.Time.dt.hour
heart_rate['minuut'] = heart_rate.Time.dt.minute
heart_rate['seconde'] = heart_rate.Time.dt.second

# gooi alles in de db:
# Id, Time, Value, jaar, maand, dag, uur, minuut, seconde

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
    db = os.path.join('..', 'db', 'main.db')

    # create tables
    sql_create_heartrate_table = """CREATE TABLE IF NOT EXISTS heartrate (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                patient int NOT NULL,
                                value int NOT NULL,
                                year int NOT NULL,
                                month int NOT NULL,
                                day int NOT NULL,
                                hour int NOT NULL,
                                minute int NOT NULL,
                                second int NOT NULL); """

    sql_insert_dummy_heartrate = """INSERT INTO heartrate (patient, value, year, month, day, hour, minute, second)
                             VALUES
                             (2, ?, ?, ?, ?, ?, ?, ?);"""

    conn = create_connection(db)

    if conn is not None:
        create_table(conn, sql_create_heartrate_table)

        heart_rate = heart_rate.drop(columns=['Id', 'Time'])

        query = """INSERT INTO heartrate (patient, value, year, month, day, hour, minute, second)
                VALUES
                """
        
        for index, row in heart_rate.iterrows():
            # do(conn, sql_insert_dummy_heartrate, *row)
            query += """(2, {}, {}, {}, {}, {}, {}, {})""".format(*row)

            if index != len(heart_rate) - 1:
                query += """,
            """ 
            else:
                query += """;"""
                break

            if index % 100000 == 0:
                print(index)

        do(conn, query)

    else:
        print("Error! cannot create the database connection.")

    conn.close()



