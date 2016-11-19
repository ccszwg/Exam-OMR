import csv
import sqlite3

db = sqlite3.connect(':memory:')


def init_db(cur):
    cur.execute('''CREATE TABLE classes (
        Row INTEGER,
        Name TEXT,
        Year INTEGER,
        Priority INTEGER)''')


def populate_db(cur, csv_fp):
    rdr = csv.reader(csv_fp)
    cur.executemany('''
        INSERT INTO foo (Row, Name, Year, Priority)
        VALUES (?,?,?,?)''', rdr)


cur = db.cursor()
init_db(cur)
populate_db(cur, open('../data/classes.cvs'))
db.commit()
