"""
Trivia game module for rikka.
The format for the leaderbaord is as follows:
    ServerID, UserID, Score
Carlos Saucedo, 2018
"""
from random import randint
from Mods.triviaSet import triviaSet
from Mods.triviaScore import triviaScore
import re, sqlite3, datetime
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
        conn = sqlite3.connect("db/database.db")
        c = conn.cursor()

        c.execute("SELECT score FROM leaderboard\n"
            + "WHERE user='" + str(userID) + "';")
        score = c.fetchone()[0]
        c.close()
        return score
        
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

    def addPoints(self, serverID, userID, amount):
        # Instantiate the sqlite variable
        conn = sqlite3.connect("db/database.db")
        c = conn.cursor()

        # Search for the entries
        #TODO: More efficient?
        c.execute("SELECT * FROM leaderboard WHERE user='"+str(userID)+"';")
        if(len(c.fetchall()) == 0):
            # If the entry does not exist
            c.execute('''
            INSERT INTO leaderboard
            VALUES (''' + "'"  + str(serverID) + "', '" + str(userID) + "', '" + str(amount) + "', '"
            + str(datetime.datetime.now().isoformat()) + "');")
        else:
            c.execute("SELECT * FROM leaderboard WHERE user='"+str(userID)+"';")
            currentScore = c.fetchone()[2]
            c.execute("UPDATE leaderboard\n"+
                "SET score="+ str(currentScore+amount) + "\n"+
                "WHERE user='" + str(userID) + "';")
        # End the connection 
        conn.commit()   
        conn.close()

    #TODO: Do we even need this?
    def addPoint(self, serverID, userID):
        self.addPoints(serverID, userID, 1)
            
    def subtractPoints(self, serverID, userID, amount):
        self.addPoints(serverID, userID, (amount * -1))
            
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
        conn = sqlite3.connect("db/database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM leaderboard ORDER BY score DESC;")
        globalScores = c.fetchall()
        c.close()

        return globalScores

    def getLocalLeaderboard(self, serverID):
        conn = sqlite3.connect("db/database.db")
        c = conn.cursor()
        
        c.execute("SELECT * FROM leaderboard WHERE server='" + str(serverID) + "' ORDER BY score DESC;")
        localScores = c.fetchall()
        c.close()
        
        return localScores
