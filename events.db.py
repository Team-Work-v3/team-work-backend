import sqlite3

conn = sqlite3.connect('library_site.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        login TEXT NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        location TEXT NOT NULL,
                        created_by INTEGER,
                        FOREIGN KEY (created_by) REFERENCES users(id))''')

conn.commit()
conn.close()

def getUserID(user_id):
    conn = sqlite3.connect('library_site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def getUser(login):
    conn = sqlite3.connect('library_site.db')
    cursor = conn.cursor()
    cursor.execute('SELECT login FROM users WHERE login = ?', (login,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def addEvent(user_id, name, description, date, time, location):

    conn = sqlite3.connect('library_site.db')
    cursor = conn.cursor()

    cursor.execute('SELECT role FROM users WHERE user_id = ?',(user_id,))
    result = cursor.fetchone()

    if not result or result[0] != 'admin':
        conn.close()
        return False

    cursor.execute('''INSERT INTO events (name, description, date, time, location, created_by) 
    VALUES (?, ?, ?, ?, ?, ?)''', (name, description, date, time, location, user_id))

    conn.commit()
    conn.close()
    return True

