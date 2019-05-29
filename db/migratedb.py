import sqlite3

conn = sqlite3.connect("database.db")

c = conn.cursor()

leaderboardFile = open("../leaderboard.txt")
leaderboardList = leaderboardFile.read().splitlines()
leaderboardFile.close()

for line in leaderboardList:
    splitline = line.split()
    c.execute('''INSERT INTO leaderboard
    VALUES ('''+ splitline[0] + ", " + splitline[1] + ", " + splitline[2]+");")

conn.commit()
conn.close()