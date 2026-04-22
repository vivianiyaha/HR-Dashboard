import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT,
                    password TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
                    username TEXT,
                    attrition REAL,
                    performance REAL,
                    kpi REAL,
                    decision TEXT
                )''')
    conn.commit()
