"""
Dataset for storing a user's score, server, and userID.
Carlos Saucedo, 2018
"""

class triviaScore:
    def __init__(self, guildID, userID, score):
        self.guildID = guildID
        self.userID = userID
        self.score = score
        
    def getGuild(self):
        return self.guildID
    
    def getUser(self):
        return self.userID
    
    def getScore(self):
        return self.score