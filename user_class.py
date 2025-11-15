from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id=None, dbase=None, db_user=None):
        if db_user:
            self.user = db_user
        else:
            self.user = dbase.getUser(user_id)
