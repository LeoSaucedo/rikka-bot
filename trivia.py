"""
Trivia game module for rikka.
The format for the leaderbaord is as follows:
    ServerID, UserID, Score
Carlos Saucedo, 2018
"""
from random import randint
from triviaSet import triviaSet
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
        self.questionNumber = None
        
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
                questionNumber = randint(0, self.questionCount -1)
                question = self.questionList[questionNumber]
                question = question.decode("utf-8")
                answer = self.answerList[questionNumber]
                answer = answer.decode("utf-8")
                x.setQuestion(question, answer)
                return x.getQuestion()
        if inList == False:
            #The server has not initated a trivia game.
            questionNumber = randint(0, self.questionCount -1)
            question = self.questionList[questionNumber]
            question = question.decode("utf-8")
            answer = self.answerList[questionNumber]
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
            
    def format(self, attempt):
        #Formats an attempt to make it easier to guess.
        #Removes "the", "a", "an", and any parenthetical words.
        formatted = attempt.lower()
        words = formatted.split()
        for word in words:
            if word == "the":
                words.remove(word)
            if word == "a":
                words.remove(word)
            if word == "an":
                words.remove(word)
        index = 0
        for word in words:
            if word.startswith("("):
                shortwords = words[:words.list(word)]
                words = shortwords
            else:
                index+= 1
        
        for word in words:
            formatted = ""
            formatted+= word + " "
        return formatted
        
        