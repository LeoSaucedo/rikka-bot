"""
Wolfram API implementation for Python.
Returns queries as a text file.
Carlos Saucedo, 2019
"""
import wolframalpha


class Client(object):
    def __init__(self, key):
        self.key = key
        self.client = wolframalpha.Client(key)

    # Processes a user query.
    def ask(self, queryText):
        res = self.client.query(queryText)
        return next(res.results).text
