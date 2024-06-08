# create_db.py
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE complaints
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          phone TEXT NOT NULL,
          complaint TEXT NOT NULL)
          ''')
conn.commit()
conn.close()
