from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id=False, dbase=False, db_user=False):
        if db_user:
            self.user = db_user
        else:
            self.user = dbase.getUserID(user_id)
