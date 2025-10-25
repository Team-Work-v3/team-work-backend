from events import LibraryDB

login, password, access_level = input("Input: login password access_level\n").split()
LibraryDB().addUser(login, password, access_level)