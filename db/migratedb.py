import sqlite3
import datetime

conn = sqlite3.connect("database.db")

c = conn.cursor()


c.execute('''
CREATE TABLE leaderboard(
    server varchar(20),
    user varchar(20),
    score int,
    collectionDate text
)
''')

leaderboardFile = open("../leaderboard.txt")
leaderboardList = leaderboardFile.read().splitlines()
leaderboardFile.close()

for line in leaderboardList:
    splitline = line.split()
    c.execute('''INSERT INTO leaderboard
    VALUES ('''+ "'" + splitline[0] + "', '" + splitline[1] + "', '" + splitline[2]+"', '" + str(datetime.datetime.now().isoformat()) +"');")

conn.commit()
conn.close()