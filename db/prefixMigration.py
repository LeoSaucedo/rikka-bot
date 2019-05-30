"""
Prefix database migration program for Rikka.
Carlos Saucedo, 2019
"""

import sqlite3
import datetime

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute('''
CREATE TABLE prefixes(
    server varchar(20),
    prefix text
);
''')

prefixFile = open("../server_prefixes.txt", "r")
prefixList = prefixFile.read().split("\n")
prefixFile.close()

for line in prefixList:
    splitline = line.split()
    c.execute("INSERT INTO prefixes VALUES (?, ?)", (splitline[0], splitline[1]))

conn.commit()
conn.close()