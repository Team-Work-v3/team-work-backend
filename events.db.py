import sqlite3


class LibraryDBCreator:
    def __init__(self, db_name='library_site.db'):
        self.db_name = db_name
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()

    def createUsersTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                login TEXT NOT NULL,
                                password TEXT NOT NULL,
                                role TEXT NOT NULL)''')
        self.connector.commit()

    def createEventsTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                description TEXT,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL,
                                location TEXT NOT NULL,
                                created_by INTEGER,
                                FOREIGN KEY (created_by) REFERENCES users(user_id))''')
        self.connector.commit()

    def __del__(self):
        self.connector.close()

class LibraryDB:
    def __init__(self, db_name='library_site.db'):
        self.db_name = db_name
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()

    def getUserID(self, user_id):
        self.cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def getUser(self, login):
        self.cursor.execute('SELECT login FROM users WHERE login = ?', (login,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def addEvent(self, user_id, name, description, date, time, location):

        self.cursor.execute('SELECT role FROM users WHERE user_id = ?',(user_id,))
        result = self.cursor.fetchone()

        if not result or result[0] != 'admin':
            return False

        self.cursor.execute('''INSERT INTO events (name, description, date, time, location, created_by) 
        VALUES (?, ?, ?, ?, ?, ?)''', (name, description, date, time, location, user_id))

        self.connector.commit()
        return True

    def __del__(self):
        self.connector.close()


if __name__ == "__main__":
    LibraryDBCreator().createUsersTable()
    LibraryDBCreator().createEventsTable()


