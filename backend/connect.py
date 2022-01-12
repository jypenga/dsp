import sqlite3
import functools

from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(db_file)
        print(e)

    return conn

def with_connection(db):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = create_connection(db)
            response = func(conn, *args, **kwargs)
            conn.commit()
            conn.close()
            return response
        return wrapper
    return decorator