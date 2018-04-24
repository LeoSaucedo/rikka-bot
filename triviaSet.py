"""
Dataset for storing trivia instances.
Stores serverID, question, and answer.
Carlos Saucedo, 2018
"""
import trivia
class triviaSet:
    def __init__(self, serverID):
        self.serverID = serverID
    
    def setQuestion(self, question, answer):
        self.question = question
        self.answer = answer
        
    def setSent(self, sent):
        self.isSent = sent
        
    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.answer
    
    def getServer(self):
        return self.serverID
    
    def getSent(self):
        return self.isSent