"""
Trivia game module for rikka.
The format for the leaderbaord is as follows:
    ServerID, UserID, Score
Carlos Saucedo, 2018
"""
from random import randint
from Mods.triviaSet import triviaSet
from Mods.triviaScore import triviaScore
import re
from array import array
class triviaGame:
    def __init__(self, questionPath, answerPath):
        leaderboardFile = open("leaderboard.txt", "r")
        self.leaderboardList = leaderboardFile.read().splitlines()
        leaderboardFile.close()
        
        questionFile = open(questionPath, "r", encoding="utf8")
        self.questionList = questionFile.read().encode("ascii", "ignore").splitlines()
        self.questionCount = len(self.questionList)
        questionFile.close()
        
        answerFile = open(answerPath, "r", encoding="utf8")
        self.answerList = answerFile.read().encode("ascii", "ignore").splitlines()
        answerFile.close()
        
        self.setList = []
        
    def getQuestionCount(self):
        return self.questionCount
        
    def getQuestion(self, serverID):
        #Returns a randomly selected question.
        inList = False
        for x in self.setList:
            if x.getServer() == serverID:
                #If the server has already started a question instance.
                inList = True
                self.questionNumber = randint(0, self.questionCount -1)
                question = self.questionList[self.questionNumber]
                question = question.decode("utf-8")
                answer = self.answerList[self.questionNumber]
                answer = answer.decode("utf-8")
                x.setQuestion(question, answer)
                return x.getQuestion()
        if inList == False:
            #The server has not initated a trivia game.
            self.questionNumber = randint(0, self.questionCount -1)
            question = self.questionList[self.questionNumber]
            question = question.decode("utf-8")
            answer = self.answerList[self.questionNumber]
            answer = answer.decode("utf-8")
            x = triviaSet(serverID)
            x.setQuestion(question, answer)
            self.setList.append(x)
            return x.getQuestion()
            
    def getAnswer(self, serverID):
        #Returns the answer to the given question.
        for x in self.setList:
            if x.getServer() == serverID:
                return x.getAnswer()
    
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
        
    def getSent(self, serverID):
        inList = False
        for x in self.setList:
            if x.getServer() == serverID:
                inList = True
                return x.getSent()
        if inList == False:
            return False
        
    def setSent(self, serverID, state):
        for x in self.setList:
            if x.getServer() == serverID:
                x.setSent(state)
        
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
                self.newPoints = currentPoints + 1
                userInList = True # User is in leaderboard.
                #Replace line in leaderboard file
                leaderboardList = open("leaderboard.txt").read().splitlines()
                leaderboardList[index] = self.server + " " + self.user + " " + str(self.newPoints)
                open("leaderboard.txt", "w").write("\n".join(leaderboardList))
            index = index + 1
    
    def addPoints(self, serverID, userID, amount):
        #Adds a set amount of points to the given user's score
        #FIXME: New users are given incorrect score.s
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
                self.newPoints = currentPoints + amount
                userInList = True # User is in leaderboard.
                #Replace line in leaderboard file
                leaderboardList = open("leaderboard.txt").read().splitlines()
                leaderboardList[index] = self.server + " " + self.user + " " + str(self.newPoints)
                open("leaderboard.txt", "w").write("\n".join(leaderboardList))
            index = index + 1    
    
        if userInList == False:
            #User is not in the leaderboard.
            leaderboardFile = open("leaderboard.txt", "a+")
            leaderboardFile.write("\n" + str(serverID) + " " + str(userID) + " " + str(self.newPoints))
            leaderboardFile.close()
            
    def subtractPoints(self, serverID, userID, amount):
        #Adds a set amount of points to the given user's score
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
                self.newPoints = currentPoints - amount
                userInList = True # User is in leaderboard.
                #Replace line in leaderboard file
                leaderboardList = open("leaderboard.txt").read().splitlines()
                leaderboardList[index] = self.server + " " + self.user + " " + str(self.newPoints)
                open("leaderboard.txt", "w").write("\n".join(leaderboardList))
            index = index + 1    
    
        if userInList == False:
            #User is not in the leaderboard.
            leaderboardFile = open("leaderboard.txt", "a+")
            leaderboardFile.write("\n" + str(serverID) + " " + str(userID) + " " + str(self.newPoints*-1))
            leaderboardFile.close()   
            
    def format(self, attempt):
        #Formats an attempt to make it easier to guess.
        #Removes "the", "a", "an", and any parenthetical words.
        formatted = attempt.lower()
        if attempt.startswith("a "):
            formatted = formatted.replace("a ", "")
        if attempt.startswith("the "):
            formatted = formatted.replace("the ","")
        if attempt.startswith("an "):
            formatted = formatted.replace("an ", "")
        formatted = re.sub("[\(\[].*?[\)\]]", "", formatted)
        return formatted
    
    def flag(self):
        #Adds the current question to the list of flagged questions.
        flaggedFile = open("flagged_questions.list", "a+")
        flaggedFile.write(str(self.questionNumber))
        flaggedFile.close()
        
    def getGlobalLeaderboard(self):
        leaderboardFile = open("leaderboard.txt", "r")
        self.leaderboardList = leaderboardFile.read().splitlines()
        leaderboardFile.close()
        globalScores = []
        
        #Adding all of the scores into the unsorted array.
        i = 1
        while i < len(self.leaderboardList):
            splitLine = self.leaderboardList[i].split()
            newSet = triviaScore(splitLine[0], splitLine[1], splitLine[2])
            globalScores.append(newSet)
            i += 1
        #Sorting elements in previously created array.
        n = len(globalScores)
        for i in range(n):
            for j in range(0, n-i-1):
                if int(globalScores[j].getScore()) < int(globalScores[j+1].getScore()):
                    globalScores[j], globalScores[j+1] = globalScores[j+1], globalScores[j]
        return globalScores
    
    def getLocalLeaderboard(self, serverID):
        leaderboardFile = open("leaderboard.txt", "r")
        self.leaderboardList = leaderboardFile.read().splitlines()
        leaderboardFile.close()
        localScores = []
        server = str(serverID)
        i = 1
        while i < len(self.leaderboardList):
            splitline = self.leaderboardList[i].split()
            if splitline[0] == server:
                newSet = triviaScore(splitline[0], splitline[1], splitline[2])
                localScores.append(newSet)
            i += 1
        
        #Sorting elements in previously created array.
        n = len(localScores)
        for i in range(n):
            for j in range(0, n-i-1):
                if int(localScores[j].getScore()) < int(localScores[j+1].getScore()):
                    localScores[j], localScores[j+1] = localScores[j+1], localScores[j]
        return localScores            
        
