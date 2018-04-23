"""
Trivia game module for rikka.
The format for the leaderbaord is as follows:
    ServerID, UserID, Score
Carlos Saucedo, 2018
"""
from random import randint
import discord
from discord import message

class triviaGame:
    def __init__(self, questionPath, answerPath):
        leaderboardFile = open("leaderboard.txt", "r")
        self.leaderboardList = leaderboardFile.read().splitlines()
        leaderboardFile.close()
        
        questionFile = open(questionPath, "r")
        self.questionList = questionFile.read().splitlines()
        self.questionCount = len(self.questionList)
        questionFile.close()
        
        answerFile = open(answerPath, "r")
        self.answerList = answerFile.read().splitlines()
        answerFile.close()
        self.questionNumber = None
        
    def getQuestion(self):
        #Returns a randomly selected question.
        self.questionNumber = randint(0, self.questionCount -1)
        return self.questionList[self.questionNumber]
        
    def getAnswer(self):
        #Returns the answer to the given question.
        self.isQuestionSent = False
        return self.answerList[self.questionNumber]
    
    def getScore(self, userID):
        #Returns the score for the author of the message.
        leaderboardFile = open("leaderboard.txt", "r")
        self.leaderboardList = leaderboardFile.read().splitlines()
        leaderboardFile.close()
        self.user = str(userID)
        userInList = False
        for line in self.leaderboardList:
            splitLine = line.split()
            if splitLine[1] == self.user:
                userInList = True
                return splitLine [2]
        if userInList == False:
            return 0
        
    def getCorrect(self):
        return self.isCorrect
    
    def getSent(self):
        return self.isQuestionSent
        
    def addPoint(self, serverID, userID):
        #Adds a point to the given user's score.
        leaderboardFile = open("leaderboard.txt", "r")
        self.leaderboardList = leaderboardFile.read().splitlines()
        leaderboardFile.close()
        userInList = False
        index = 0
        self.user = str(userID)
        self.server = str(serverID)
        for line in self.leaderboardList:
            splitLine = line.split()
            if splitLine[1] == self.user:
                self.server = splitLine[0]
                currentPoints = int(splitLine[2])
                newPoints = currentPoints + 1
                userInList = True # User is in leaderboard.
                #Replace line in leaderboard file
                leaderboardList = open("leaderboard.txt").read().splitlines()
                leaderboardList[index] = self.server + " " + self.user + " " + str(newPoints)
                open("leaderboard.txt", "w").write("\n".join(leaderboardList))
            index = index + 1
        
        if userInList == False:
            #User is not in the leaderboard.
            leaderboardFile = open("leaderboard.txt", "a+")
            leaderboardFile.write("\n" + str(serverID) + " " + str(userID) + " " + "1")
            leaderboardFile.close()
        
        
        
        
        
        