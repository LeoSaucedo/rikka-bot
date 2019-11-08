"""
Trivia game module for rikka.
Carlos Saucedo, 2019
"""
from random import randint
from Mods.triviaSet import triviaSet
from Mods.triviaScore import triviaScore
import re
import sqlite3
import datetime
from array import array


class triviaGame:
    def __init__(self):
        conn = sqlite3.connect("db/database.db")
        c = conn.cursor()
        c.execute("SELECT question FROM trivia")
        self.questionList = c.fetchall()
        self.questionCount = len(self.questionList)

        c.execute("SELECT answer FROM trivia")
        self.answerList = c.fetchall()

        self.setList = []

    def getQuestionCount(self):
        return self.questionCount

    def getQuestion(self, serverID):
        # Returns a randomly selected question.
        inList = False
        for x in self.setList:
            if x.getServer() == serverID:
                # If the server has already started a question instance.
                inList = True
                self.questionNumber = randint(0, self.questionCount - 1)
                question = self.questionList[self.questionNumber][0]
                answer = self.answerList[self.questionNumber][0]
                x.setQuestion(question, answer)
                return x.getQuestion()
        if inList == False:
            # The server has not initiated a trivia game.
            self.questionNumber = randint(0, self.questionCount - 1)
            question = self.questionList[self.questionNumber][0]
            answer = self.answerList[self.questionNumber][0]
            x = triviaSet(serverID)
            x.setQuestion(question, answer)
            self.setList.append(x)
            return x.getQuestion()

    def getAnswer(self, serverID):
        # Returns the answer to the given question.
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
        # TODO: More efficient?
        c.execute("SELECT * FROM leaderboard WHERE user='"+str(userID)+"';")
        if(len(c.fetchall()) == 0):
            # If the entry does not exist
            c.execute('''
            INSERT INTO leaderboard
            VALUES (''' + "'" + str(serverID) + "', '" + str(userID) + "', '" + str(amount) + "', '"
                      + str(datetime.datetime.now().isoformat()) + "');")
        else:
            c.execute("SELECT * FROM leaderboard WHERE user='"+str(userID)+"';")
            currentScore = c.fetchone()[2]
            c.execute("UPDATE leaderboard\n" +
                      "SET score=" + str(currentScore+amount) + "\n" +
                      "WHERE user='" + str(userID) + "';")
        # End the connection
        conn.commit()
        conn.close()

    # TODO: Do we even need this?
    def addPoint(self, serverID, userID):
        self.addPoints(serverID, userID, 1)

    def subtractPoints(self, serverID, userID, amount):
        self.addPoints(serverID, userID, (amount * -1))

    def format(self, attempt):
        # Formats an attempt to make it easier to guess.
        # Removes "the", "a", "an", and any parenthetical words.
        formatted = attempt.lower()
        if attempt.startswith("a "):
            formatted = formatted.replace("a ", "")
        if attempt.startswith("the "):
            formatted = formatted.replace("the ", "")
        if attempt.startswith("an "):
            formatted = formatted.replace("an ", "")
        formatted = re.sub("[\(\[].*?[\)\]]", "", formatted)
        return formatted

    def flag(self):
        # Adds the current question to the list of flagged questions.
        flaggedFile = open("flagged_questions.list", "a+")
        flaggedFile.write(str(self.questionNumber))
        flaggedFile.close()

    def getGlobalLeaderboard(self):
        conn = sqlite3.connect("db/database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM leaderboard ORDER BY score DESC LIMIT 0,10;")
        globalScores = c.fetchall()
        c.close()

        return globalScores

    def getLocalLeaderboard(self, users):
        conn = sqlite3.connect("db/database.db")
        c = conn.cursor()
        usersl = "'" + "', '".join(users) + "'"
        c.execute(f'SELECT * FROM leaderboard WHERE user IN ({usersl}) ORDER BY score DESC LIMIT 0,10;')
        localScores = c.fetchall()
        c.close()
        return localScores
