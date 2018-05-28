"""
Economy module for Rikka.
Carlos Saucedo, 2018
"""

import datetime
from random import randint
import Mods.trivia as trivia

def getCurrentDay():
    now = datetime.datetime.now()
    return(str(now.day))

def hasCollectedToday(userID):
    collectionFile = open("collectiondates.txt", "r")
    collectionList = collectionFile.read().splitlines()
    collectionFile.close()
    
    userInList = False
    user = str(userID)
    for line in collectionList:
        splitLine = line.split()
        if splitLine[0] == user:
            userInList = True
            if splitLine[1] == getCurrentDay():
                return True
            else: 
                return False
    if userInList == False:
        return False
            
def setCollectionDate(userID):
    collectionFile = open("collectiondates.txt", "r")
    collectionList = collectionFile.read().splitlines()
    collectionFile.close()
    
    userInList = False
    index = 0
    user = str(userID)
    for line in collectionList:
        splitline = line.split()
        if splitline[0] == user:
            userInList = True
            collectionList = open("collectiondates.txt").read().splitlines()
            collectionList[index] = user + " " + getCurrentDay()
            open("collectiondates.txt", "w").write("\n".join(collectionList))
            
        index = index + 1
    if userInList == False:
        collectionFile = open("collectiondates.txt", "a+")
        collectionFile.write(user + " " + getCurrentDay())
        collectionFile.close()