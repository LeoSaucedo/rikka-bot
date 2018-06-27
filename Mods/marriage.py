"""
Marriage module for Rikka.
Carlos Saucedo, 2018
"""

import discord

marriageFile = open("marriages.txt", "r")
marriageList = marriageFile.read().splitlines()
marriageFile.close()

"""
Dataset representing a married couple.
Consists of 2 user IDs.
"""
class couple:
    def init(self, user1, user2):
        self.user1 = user1
        self.user2 = user1
        
    def get1(self):
        return self.user1
    
    def get2(self):
        return self.user2
    

def isMarried(user):
    """
    Checks to see if the user is married.
    A user is married if their ID is found anywhere in the list of marriages.
    """
    
    self.user = str(user)
    
    userInList = False
    for marriage in marriageList:
        splitmarriage = marriage.split()
        if (splitmarriage[0] == self.user) or (splitmarriage[1] == self.user):
            userInList = True
            
    return userInList

def newMarriage(user1, user2):
    self.user1 = user1
    self.user2 = user2
    
    if (not isMarried(self.user1) and (not isMarried(user2))):
        
    
            