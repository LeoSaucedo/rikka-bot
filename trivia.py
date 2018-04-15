"""
Trivia game module for rikka.
Carlos Saucedo, 2018
"""
from random import randint

class triviaGame:
    def __init__(self, questionPath, answerPath):
        leaderboardFile = open("leaderboard.txt", "r")
        self.leaderboardList = leaderboardFile.read().splitlines()
        leaderboardFile.close()
        
        questionFile = open(questionPath, "r")
        self.questionList = questionFile.read().splitlines()
        questionFile.close()
        
        answerFile = open(answerPath, "r")
        self.answerList = answerFile.read().splitlines()
        answerFile.close()
        
    def getScore(self, userID):
        userInList = False
        for line in self.leaderboardList:
            splitLine = line.split()
            if splitLine[2] == userID:
                userInList = True
                return splitLine [3]
        if userInList == False:
            return 0
        
    def addPoint(self, serverID, userID):
        userInList = False
        index = 0
        for line in self.leaderboardList:
            splitLine = line.split()
            if splitLine[1] == userID:
                serverID = splitLine[0]
                currentPoints = int(splitLine[2])
                newPoints = currentPoints + 1
                userInList = True # User is in leaderboard.
                leaderboardFile = open("leaderboard.txt", "w+")
                self.leaderboardList[index] = serverID + " " + userID + " " + str(newPoints)
                leaderboardFile.write("/n".join(self.leaderboardFile))
                leaderboardFile.close()
                
        if userInList == False:
            #User is not in the leaderboard.
            leaderboardFile = open("leaderboard.txt", "a+")
            leaderboardFile.write("\n" + serverID + " " + userID + " " + "1")
            leaderboardFile.close()
                
        index = index + 1