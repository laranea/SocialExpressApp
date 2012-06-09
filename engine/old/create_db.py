__author__ = 'kristof.leroux@gmail.com'

import sqlite3

conn = sqlite3.connect('socialexpress.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE feeds (id INTEGER AUTO_INCREMENT PRIMARY_KEY, text VARCHAR(63206), date TEXT, username VARCHAR(255), location VARCHAR(255))')