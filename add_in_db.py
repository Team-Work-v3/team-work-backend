from werkzeug.security import generate_password_hash
from events import LibraryDB

login, password, access_level = input("Input: login password access_level\n").split()
LibraryDB().addUser(login, generate_password_hash(password), access_level)