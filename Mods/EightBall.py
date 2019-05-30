"""
Eight Ball module for Rikka.
Carlos Saucedo, 2019
"""

from random import randint

class eightBallGenerator:
    def __init__(self):
        self.responses = [
            "it is certain.",
            "it is decidedly so.",
            "without a doubt.",
            "yes, definitely.",
            "you may rely on it.",
            "you can count on it.",
            "as I see it, yes.",
            "most likely.",
            "outlook good.",
            "yes.",
            "signs point to yes.",
            "absolutely.",
            "reply hazy, try again.",
            "ask again later.",
            "better not tell you now.",
            "cannot predict now.",
            "concentrate and ask again.",
            "don't count on it.",
            "my reply is no.",
            "my sources say no.",
            "outlook not so good.",
            "very doubtful.",
            "chances aren't good."
            ]

    def getAnswer(self):
        responseIndex = randint(0, len(self.responses)-1)
        return self.responses[responseIndex]