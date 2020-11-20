import sqlite3
import os
from sqlite3 import Error

DB_FILE = r'db/pysqlite.db'


def create_tables(conn):
    create_postings_table = ''' CREATE TABLE IF NOT EXISTS Postings (
                                        pid int PRIMARY KEY, 
                                        title text NOT NULL,
                                        price int NOT NULL,
                                        link text NOT NULL,
                                        entry_date text NOT NULL
                                    ); '''
    try:
        cursor = conn.cursor()
        cursor.execute(create_postings_table)
    except Error as e:
        print(e)


def create_connection():
    conn = None

    try:
        conn = sqlite3.connect(DB_FILE)
    except Error as e:
        print(e)
    return conn


def main():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w'): pass

    conn = create_connection()

    if conn is not None:
        create_tables(conn)
    else:
        print('Cannot connect to database.')


if __name__ == '__main__':
    main()
