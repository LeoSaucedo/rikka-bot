"""
A simple class that allows a server to set their own prefix.
"""
class serverPrefix(object):
    def __init__(self, serverID, prefix):
        self.prefix = prefix
        self.serverID = serverID
    
    def setPrefix(self, newPrefix):
        self.prefix = newPrefix
        
    def setID(self, newID):
        self.serverID, newID
        
    def getPrefix(self):
        return self.prefix
    
    def getID(self):
        return self.serverID