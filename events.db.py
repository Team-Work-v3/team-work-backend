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
                                access_level TEXT NOT NULL,
                                is_active INTEGER NOT NULL DEFAULT 1)''')
        self.connector.commit()

    def createEventsTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                info TEXT,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL,
                                location TEXT NOT NULL,
                                max_places INTEGER NOT NULL,
                                price REAL NOT NULL,
                                image TEXT,
                                is_active INTEGER NOT NULL DEFAULT 1,
                                created_by INTEGER NOT NULL,
                                FOREIGN KEY (created_by) REFERENCES users(user_id))''')
        self.connector.commit()

    def __del__(self):
        self.connector.close()

class LibraryDB:
    def __init__(self, db_name='library_site.db'):
        self.db_name = db_name
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()

#users_db

    def addUser(self, login, password, access_level, is_active=True):
        password_hash = generate_password_hash(password)

        self.cursor.execute('''
            INSERT INTO users (login, password_hash, access_level, is_active)
            VALUES (?, ?, ?, ?)
        ''', (login, password_hash, access_level, int(is_active)))

        self.connector.commit()

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

    def isUserActive(self, user_id):
        self.cursor.execute('SELECT is_active FROM users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return True
        else:
            return False

    def getAccessLevel(self, user_id):
        self.cursor.execute('SELECT access_level FROM users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return True
        else:
            return False

#events_db

    def addEvent(self, name, info, date, time, location, max_places, price, image, is_active=True):

        self.cursor.execute('''
                INSERT INTO events (
                    name_event, info, date, time, location,
                    max_places, price, image, is_active, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name_event, info, date, time, location,
                  max_places, price, image, active, created_by))
        self.connector.commit()
        return True

    def getEvent(self, event_id):
        self.cursor.execute('SELECT * FROM events WHERE id_event = ?', (event_id,))
        return self.cursor.fetchone()

    def update_event(self, event_id, name_event=None, info=None, date=None, time=None,
                     location=None, max_places=None, price=None, image=None,
                     is_active=None, created_by=None):

        fields = []
        values = []

        if name_event is not None:
            fields.append('name_event = ?')
            values.append(name_event)
        if info is not None:
            fields.append('info = ?')
            values.append(info)
        if date is not None:
            fields.append('date = ?')
            values.append(date)
        if time is not None:
            fields.append('time = ?')
            values.append(time)
        if location is not None:
            fields.append('location = ?')
            values.append(location)
        if max_places is not None:
            fields.append('max_places = ?')
            values.append(max_places)
        if price is not None:
            fields.append('price = ?')
            values.append(price)
        if image is not None:
            fields.append('image = ?')
            values.append(image)
        if is_active is not None:
            fields.append('active = ?')
            values.append(is_active)
        if created_by is not None:
            fields.append('created_by = ?')
            values.append(created_by)

        if not fields:
            return False

        values.append(event_id)
        update = f"UPDATE events SET {', '.join(fields)} WHERE id_event = ?"

        self.cursor.execute(update, values)
        self.connector.commit()

#registration_db
    def __del__(self):
        self.connector.close()


if __name__ == "__main__":
    LibraryDBCreator().createUsersTable()
    LibraryDBCreator().createEventsTable()


