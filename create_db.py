import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            complaint TEXT NOT NULL,
            cafe_id INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
