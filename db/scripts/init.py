import os

import bcrypt
import sqlite3
import random

import numpy as np
import pandas as pd
import datetime as dt

from sqlite3 import Error
from datetime import datetime

# score function
def score(df):
    
    score = []
    
    # mean and std
    steps_mean = df.Steps.mean()
    steps_std = df.Steps.std()
    
    heart_rate_mean = df.HR.mean()
    heart_rate_std = df.HR.std()
    
    sleep_mean = df.Sleep.mean()
    sleep_std = df.Sleep.std()
    
    for index, row in df.iterrows():
        
        count = 0
        
        # steps
        if row.Steps < (steps_mean - steps_std):
            count += 1
        elif row.Steps > (steps_mean + steps_std):
            count += 3
        else:
            count += 2
        
        # heart rate
        if row.HR < 40:
            count += 1
        elif row.HR < heart_rate_mean:
            count += 3
        elif row.HR >= heart_rate_mean and row.HR <= (heart_rate_mean + 3*heart_rate_std): # three std to be safe
            count += 2
        else:
            count += 1
        
        # sleep
        if row.Sleep < (sleep_mean - sleep_std):
            count += 1
        elif row.Sleep > (sleep_mean + sleep_std):
            count += 3
        else:
            count += 2
        
        # bp upper
        if row.Bp_upper < 100:
            count += 1
        elif row.Bp_upper < 135:
            count += 3
        elif row.Bp_upper >= 135 and row.Bp_upper <= 160:
            count += 2
        elif row.Bp_upper > 160:
            count += 1
        
        # bp lower
        if row.Bp_lower < 60:
            count += 1
        elif row.Bp_lower < 85:
            count += 3
        elif row.Bp_lower >= 85 and row.Bp_lower <= 100:
            count += 2
        else:
            count += 1
            
        if count < 10:
            score.append(1)
        elif count > 12: 
            score.append(3)
        else: 
            score.append(2)
            
    return score


# load data in one pd.DataFrame
def load_all_csv(root='../../Data', pid=5553957443):
    # heart rate per second
    heart_rate = pd.read_csv(os.path.join(root, 'heartrate_seconds_merged.csv'))
    heart_rate.Time = heart_rate.Time.apply(lambda s: datetime.strptime(s, '%m/%d/%Y %I:%M:%S %p'))

    # only select heart rates between 07:00 and 22:00
    heart_rate = heart_rate.iloc[pd.DatetimeIndex(heart_rate['Time']).indexer_between_time('7:00:00','22:00:00')]
    heart_rate = heart_rate[heart_rate.Id == pid]

    # keep original for plots
    heart_rate_plots = heart_rate.copy()

    # transform heart_rate per second to heart rate per minute
    heart_rate.index = heart_rate.Time
    heart_rate_minute = pd.DataFrame(heart_rate.groupby(heart_rate.index.to_period('T')).Value.mean())
    heart_rate_minute.index = heart_rate_minute.index.strftime('%m/%d/%Y %H:%M') # format date to / instead of -  

    # steps per minute
    steps = pd.read_csv(os.path.join(root, 'minuteStepsNarrow_merged.csv'))
    steps.ActivityMinute = steps.ActivityMinute.apply(lambda s: datetime.strptime(s, '%m/%d/%Y %I:%M:%S %p'))

    # only select steps between 07:00 and 22:00 
    steps = steps.iloc[pd.DatetimeIndex(steps['ActivityMinute']).indexer_between_time('07:00:00', '22:00:00')]
    steps = steps[steps.Id == pid]
    steps.index = steps.ActivityMinute.dt.strftime('%m/%d/%Y %H:%M')
    steps_minute = pd.DataFrame(steps.Steps)

    # sleep per night (one night before)
    sleep = pd.read_csv(os.path.join(root, 'sleepDay_merged.csv'))
    sleep.SleepDay = sleep.SleepDay.apply(lambda s: datetime.strptime(s, '%m/%d/%Y %I:%M:%S %p'))
    sleep = sleep[sleep.Id == pid]
    sleep['Hours'] = round(sleep.TotalMinutesAsleep / 60, 2)
    sleep.SleepDay = sleep.SleepDay.dt.strftime('%m/%d/%Y')
    
    # merge the csv files
    df = pd.merge(steps_minute, heart_rate_minute, left_index=True, right_index=True, how='inner')
    df = df.rename(columns={'Value':'HR'})
    df['HR'] = df.HR.apply(lambda s: round(s)) # integer 

    # bp normal 100 - 135, preventative 135 - 160, bp real bad > 160
    df['Bp_upper'] = [random.randint(80, 200) for x in range(df.shape[0])]
    # bp normal 60 - 85, preventative 85 - 100, real bad > 100
    df['Bp_lower'] = [random.randint(50, 120) for x in range(df.shape[0])]

    # create list to add to df
    sleep_hours = {row.SleepDay: row.Hours for index, row in sleep.iterrows()}
    sleep_per_night = [sleep_hours[date[0]] for date in df.index.str.split()]

    df['Sleep'] = sleep_per_night # add sleep

    # split datetime for database
    dt_temp = pd.to_datetime(df.index)

    df['Month'] = dt_temp.month
    df['Day'] = dt_temp.day
    df['Year'] = dt_temp.year
    df['Hour'] = dt_temp.hour
    df['Minute'] = dt_temp.minute

    # call score and add new column
    df['Score'] = score(df)

    # so I can still work with datetime
    df['Date'] = pd.to_datetime(df.index, format='%m/%d/%Y %H:%M')

    # hier moet alleen nog score bij
    df = df[['Date', 'Month', 'Day', 'Year', 'Hour', 'Minute', 'Steps', 'HR', 'Sleep', 'Bp_upper', 'Bp_lower', 'Score']]

    return df


# create SQL connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


# create table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


# do SQL query
def do(conn, sql, *args):
    try:
        c = conn.cursor()
        c.execute(sql, (*args,))
        conn.commit()
    except Error as e:
        print(e)

# load df
def load(df, pid):
    query = """INSERT INTO data (patient, month, day, year, hour, minute, steps, heartrate, sleep, bp_upper, bp_lower, score)
                VALUES
                """
        
    for index, row in df.iterrows():
        # do(conn, sql_insert_dummy_heartrate, *row)
        query += """({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(pid, *row)

        if index != len(df) - 1:
            query += """,
        """ 
        else:
            query += """;"""
            break

    do(conn, query)


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
                                   avatar text,
                                   score real,
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
                                time_start text,
                                time_end text,
                                meal integer NOT NULL,
                                specific integer,
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

    sql_create_data_table = """CREATE TABLE IF NOT EXISTS data (
                              id integer PRIMARY KEY AUTOINCREMENT,
                              patient integer NOT NULL,
                              data text NOT NULL,
                              month integer NOT NULL,
                              day integer NOT NULL,
                              year integer NOT NULL,
                              hour integer NOT NULL,
                              minute integer NOT NULL,
                              steps integer NOT NULL,
                              heartrate integer NOT NULL,
                              sleep real NOT NULL,
                              bp_upper integer NOT NULL,
                              bp_lower integer NOT NULL,
                              score integer NOT NULL);"""

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
                                (2, "Anouk Hooijschuur", 2, "v", 1.70, 60.4, "avatar-f.png", 0),
                                (2, "Vera Verbanescu", 42, "v", 1.76, 70.9, "avatar-f.png", 0);"""

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

        data_a = load_all_csv(pid=5553957443)
        data_b = load_all_csv(pid=6962181067)

        load(data_a, 1)
        load(data_b, 2)
    else:
        print("Error! cannot create the database connection.")

    conn.close()