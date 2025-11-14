import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class LibraryDBCreator:
    def __init__(self, db_name='library_site.db'):
        self.db_name = db_name
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()

    def createUsersTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                login TEXT NOT NULL,
                                password_hash TEXT NOT NULL,
                                access_level TEXT NOT NULL,
                                is_active INTEGER NOT NULL DEFAULT 1)''')
        self.connector.commit()

    def createEventsTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name_event TEXT NOT NULL,
                                info TEXT,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL,
                                location TEXT NOT NULL,
                                max_places INTEGER NOT NULL,
                                price REAL NOT NULL,
                                category TEXT,
                                image TEXT,
                                is_active INTEGER NOT NULL DEFAULT 1,
                                created_by INTEGER NOT NULL,
                                FOREIGN KEY (created_by) REFERENCES users(user_id))''')
        self.connector.commit()

    def createRegistrationsTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS registration (
                                id_registration INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_event INTEGER NOT NULL,
                                full_name TEXT NOT NULL,
                                email TEXT NOT NULL,
                                phone_number TEXT,
                                agreement INTEGER,
                                FOREIGN KEY (id_event) REFERENCES events(event_id))''')
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

    def getUser(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result
        return None

    def getUserByLogin(self, login):
        self.cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        result = self.cursor.fetchone()
        if result:
            return result
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
        if result:
            return result[0]
        else:
            return False

#events_db

    def addEvent(self, name_event, info, date, time, location, max_places, price, category, image, created_by, is_active=True):

        self.cursor.execute('''
                INSERT INTO events (
                    name_event, info, date, time, location,
                    max_places, price, category, image, is_active, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name_event, info, date, time, location,
                  max_places, price, category, image, is_active, created_by))
        self.connector.commit()
        return True

    def getEvent(self, event_id):
        self.cursor.execute('SELECT * FROM events WHERE id_event = ?', (event_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return True
        else:
            return False

    def getEvents(self):
        rows = self.cursor.execute('''
            SELECT event_id, name_event, info, date, time, location,
                   max_places, price, category, image, is_active, created_by
            FROM events
        ''').fetchall()
        return rows



    def updateEvent(self, event_id, name_event=None, info=None, date=None, time=None,
                     location=None, max_places=None, price=None, category=None, image=None,
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
        if category is not None:
            fields.append('category = ?')
            values.append(category)
        if image is not None:
            fields.append('image = ?')
            values.append(image)
        if is_active is not None:
            fields.append('is_active = ?')
            values.append(is_active)
        if created_by is not None:
            fields.append('created_by = ?')
            values.append(created_by)

        if not fields:
            return False

        values.append(event_id)
        update = f"UPDATE events SET {', '.join(fields)} WHERE event_id = ?"

        print(update)
        print(values)
        self.cursor.execute(update, (name_event, info, date, time, location, max_places, price,category, image, is_active, created_by, event_id))
        self.connector.commit()
        return True

#registration_db

    def addRegistration(self, id_event, full_name, email, phone_number, agreement):
        self.cursor.execute('SELECT event_id FROM events WHERE event_id = ?', (id_event,))
        result = self.cursor.fetchone()
        if not result or not result[0]:
            return False

        self.cursor.execute('''
            INSERT INTO registration (
                id_event, full_name, email, phone_number, agreement
            ) VALUES (?, ?, ?, ?, ?)
        ''', (id_event, full_name, email, phone_number, agreement))
        self.connector.commit()
        return True

    def deleteRegistration(self, id_registration):
        self.cursor.execute('SELECT id_registration FROM registration WHERE id_registration = ?', (id_registration,))
        result = self.cursor.fetchone()
        if not result or not result[0]:
            return False

        self.cursor.execute('DELETE FROM registration WHERE id_registration = ?', (id_registration,))
        self.connector.commit()
        return True

    def updateRegistration(self, id_registration, full_name=None, email=None,
                           phone_number=None, agreement=None):
        fields = []
        values = []

        if full_name is not None:
            fields.append('full_name = ?')
            values.append(full_name)
        if email is not None:
            fields.append('email = ?')
            values.append(email)
        if phone_number is not None:
            fields.append('phone_number = ?')
            values.append(phone_number)
        if agreement is not None:
            fields.append('agreement = ?')
            values.append(agreement)

        if not fields:
            return False

        values.append(id_registration)
        update = f"UPDATE registration SET {', '.join(fields)} WHERE id_registration = ?"
        self.cursor.execute(update, values)
        self.connector.commit()
        return True

    def __del__(self):
        self.connector.close()


if __name__ == "__main__":
    LibraryDBCreator().createUsersTable()
    LibraryDBCreator().createEventsTable()
    LibraryDBCreator().createRegistrationsTable()
    #LibraryDB().addEvent("test", "info", "2025-12-22", "14:00", "123", 25, 100, "/123/123", "admin", "", 1)
    #LibraryDB().updateEvent(1, "test1234", "", "", "", "123", 25, 100, "/123/123", "admin", "", 1)


