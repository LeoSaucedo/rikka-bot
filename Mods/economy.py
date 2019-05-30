"""
Economy module for Rikka.
Carlos Saucedo, 2018
"""

import datetime, sqlite3
from random import randint
import Mods.trivia as trivia

def getCurrentDay():
    now = datetime.datetime.now()
    return(str(now.day))

def hasCollectedToday(userID):
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()

    c.execute("SELECT collectionDate FROM leaderboard WHERE user='" + str(userID) + "';")
    lastCollected = datetime.datetime.strptime(c.fetchone()[0], "%Y-%m-%dT%H:%M:%S.%f")
    if(datetime.datetime.date(lastCollected) == datetime.datetime.date(datetime.datetime.today())):
        conn.close()
        return True
    else:
        conn.close()
        return False
            
def setCollectionDate(userID):
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()

    c.execute("UPDATE leaderboard\n"+
        "SET collectionDate = " + str(datetime.datetime.now().isoformat()) + "\n" +
        "WHERE user='" + str(userID) + "';")
    conn.commit()
    conn.close()
