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
                                description_event TEXT,
                                date_event TEXT NOT NULL,
                                time_event TEXT NOT NULL,
                                location_event TEXT NOT NULL,
                                seats_event INTEGER NOT NULL,
                                price_event REAL NOT NULL,
                                event_category TEXT,
                                images_events TEXT,
                                organizers_event TEXT,
                                program_event TEXT,
                                fullDescription_event TEXT,
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
                                ticket_amount INTEGER DEFAULT 1,
                                confirmation INTEGER DEFAULT 0,
                                FOREIGN KEY (id_event) REFERENCES events(event_id))''')
        self.connector.commit()

    def createImageTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                unique_name TEXT NOT NULL UNIQUE)''')
        self.connector.commit()

    def createReviewsTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_registration INTEGER NOT NULL,
                                event_id INTEGER NOT NULL,
                                review_text TEXT NOT NULL,
                                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                                is_approved INTEGER DEFAULT 0,
                                FOREIGN KEY (id_registration) REFERENCES registration(id_registration),
                                FOREIGN KEY (event_id) REFERENCES events(event_id))''')
        self.connector.commit()

    def createCategoryTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                category_name TEXT NOT NULL)''')

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

    def addEvent(self, name_event, description_event, date_event, time_event,
                 location_event, seats_event, price_event, event_category,
                 images_events, organizers_event, program_event,
                 fullDescription_event, created_by, is_active=True):
        self.cursor.execute('''
                    INSERT INTO events (
                        name_event, description_event, date_event, time_event,
                        location_event, seats_event, price_event, event_category,
                        images_events, organizers_event, program_event,
                        fullDescription_event, is_active, created_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name_event, description_event, date_event, time_event,
                      location_event, seats_event, price_event, event_category,
                      images_events, organizers_event, program_event,
                      fullDescription_event, is_active, created_by))
        self.connector.commit()
        return True


    def getEvent(self, event_id):
        self.cursor.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return result
        else:
            return False

    def getEvents(self):
        rows = self.cursor.execute('''
            SELECT event_id, name_event, description_event, date_event, time_event,
                   location_event, seats_event, price_event, event_category,
                   images_events, organizers_event, program_event,
                   fullDescription_event, is_active, created_by
            FROM events
        ''').fetchall()
        return rows

    def updateEvent(self, event_id, name_event=None, description_event=None, date_event=None, time_event=None,
                    location_event=None, seats_event=None, price_event=None, event_category=None,
                    images_events=None, organizers_event=None, program_event=None,
                    fullDescription_event=None, created_by=None, is_active=None):

        fields = []
        values = []

        if name_event is not None:
            fields.append('name_event = ?')
            values.append(name_event)
        if description_event is not None:
            fields.append('description_event = ?')
            values.append(description_event)
        if date_event is not None:
            fields.append('date_event = ?')
            values.append(date_event)
        if time_event is not None:
            fields.append('time_event = ?')
            values.append(time_event)
        if location_event is not None:
            fields.append('location_event = ?')
            values.append(location_event)
        if seats_event is not None:
            fields.append('seats_event = ?')
            values.append(seats_event)
        if price_event is not None:
            fields.append('price_event = ?')
            values.append(price_event)
        if event_category is not None:
            fields.append('event_category = ?')
            values.append(event_category)
        if images_events is not None:
            fields.append('images_events = ?')
            values.append(images_events)
        if organizers_event is not None:
            fields.append('organizers_event = ?')
            values.append(organizers_event)
        if program_event is not None:
            fields.append('program_event = ?')
            values.append(program_event)
        if fullDescription_event is not None:
            fields.append('fullDescription_event = ?')
            values.append(fullDescription_event)
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
        self.cursor.execute(update, values)
        self.connector.commit()
        return True

    def deleteEvent(self, event_id):
        self.cursor.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
        self.connector.commit()
        return True

    def getImageByName(self, name):
        self.cursor.execute('SELECT * FROM events WHERE images_events = ?', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return False

#registration_db

    def getRegistrations(self):
        rows = self.cursor.execute('SELECT * FROM events').fetchall()
        return rows

    def addRegistration(self, id_event, full_name, email, phone_number, agreement, ticket_amount, confirmation):
        self.cursor.execute('SELECT event_id FROM events WHERE event_id = ?', (id_event,))
        result = self.cursor.fetchone()
        if not result or not result[0]:
            return False

        self.cursor.execute('''
            INSERT INTO registration (
                id_event, full_name, email, phone_number, agreement, ticket_amount, confirmation
            ) VALUES (?, ?, ?, ?, ?)
        ''', (id_event, full_name, email, phone_number, agreement, ticket_amount, confirmation))
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
                           phone_number=None, agreement=None, ticket_amount=None, confirmation=None):
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
        if ticket_amount is not None:
            fields.append('ticket_amount = ?')
            values.append(ticket_amount)
        if confirmation is not None:
            fields.append('confirmation = ?')
            values.append(confirmation)

        if not fields:
            return False

        values.append(id_registration)
        update = f"UPDATE registration SET {', '.join(fields)} WHERE id_registration = ?"
        self.cursor.execute(update, values)
        self.connector.commit()
        return True

    def getUsersInEvents(self):
        events = self.cursor.execute('''
            SELECT event_id, name_event
            FROM events
        ''').fetchall()

        result = []
        for event in events:
            event_id, event_name = event

            users = self.cursor.execute('''
                SELECT full_name, email, phone_number, agreement, ticket_amount, confirmation
                FROM registration
                WHERE id_event = ?
            ''', (event_id,)).fetchall()

            users_list = []
            for u in users:
                users_list.append({
                    "full_name": u[0],
                    "email": u[1],
                    "phone_number": u[2],
                    "agreement": u[3],
                    "ticket_amount": u[4],
                    "confirmation": u[5]
                })

            result.append({
                "event_id": event_id,
                "event_name": event_name,
                "users": users_list
            })

        return result
#reviews
    def addReview(self, id_registration, event_id, review_text, is_approved):
        self.cursor.execute('''
            INSERT INTO reviews (id_registration, event_id, review_text, is_approved)
            VALUES (?, ?, ?, ?)
        ''', (id_registration, event_id, review_text, is_approved))
        self.connector.commit()
        return True

    def getReviews(self):
        rows = self.cursor.execute('SELECT * FROM reviews').fetchall()
        return rows

    def deleteReview(self, review_id):
        self.cursor.execute(
            'SELECT review_id FROM reviews WHERE review_id = ?',
            (review_id,)
        )
        result = self.cursor.fetchone()

        if not result or not result[0]:
            return False

        self.cursor.execute(
            'DELETE FROM reviews WHERE review_id = ?',
            (review_id,)
        )
        self.connector.commit()
        return True

    #category

    def getCategory(self):
        rows = self.cursor.execute('SELECT * FROM category').fetchall()
        return rows
    def __del__(self):
        self.connector.close()


if __name__ == "__main__":
    LibraryDBCreator().createUsersTable()
    LibraryDBCreator().createEventsTable()
    LibraryDBCreator().createRegistrationsTable()
    LibraryDBCreator().createImageTable()
    LibraryDBCreator().createReviewsTable()
    LibraryDBCreator().createCategoryTable()
    #LibraryDB().addEvent("test", "info", "2025-12-22", "14:00", "123", 25, 100, "/123/123", "admin", "", 1)
    #LibraryDB().updateEvent(1, "test1234", "", "", "", "123", 25, 100, "/123/123", "admin", "", 1)
