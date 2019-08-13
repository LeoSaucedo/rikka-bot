# Trivia migration program for Rikka.
# Carlos Saucedo, 2019

import sqlite3

conn = sqlite3.connect("../db/database.db")

c = conn.cursor()

# Creating the table.
c.execute('''
CREATE TABLE trivia(
    question text,
    answer text
);
''')

# Processing the trivia questions/answers.
questionsFile = open("trivia_questions.list", "r")
questionsList = questionsFile.read().split("\n")
questionsFile.close()
answersFile = open("trivia_answers.list", "r")
answersList = answersFile.read().split("\n")
answersFile.close()

for i in range(len(questionsList) - 1):
    c.execute("INSERT INTO trivia VALUES(?, ?);",
              (questionsList[i], answersList[i]))

conn.commit()
conn.close()
