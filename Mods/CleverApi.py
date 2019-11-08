#!/usr/bin/python
# CleverBot.io Python API
# Author:     phl4nk
# Date:        08/02/2018
# Version:    v0.3

import requests,json,random

class Bot(object):
    def __init__(self,user,key):
        self.user = user
        self.key = key
        self.endpoint = 'https://cleverbot.io/1.0/'
        self.data = {
            'user':self.user,
            'key':self.key,
            }
        # create a session when init
        # TODO: Error handeling, etc.
        
        print("[+] Generating a session")
        
        response = requests.post(self.endpoint+'create',json=self.data)
        json_response = json.loads(response.text)
        if json_response['status'] == 'success':
            # Update and keep session running based on nick
            self.data.update({'nick':str(json_response['nick'])})
        else:
            print("[!] Failed to generate a session!")
            return

    # Query the API and spit back response
    def ask(self,text):
        self.data.update({'text':text})
        response = requests.post(self.endpoint+'ask', json=self.data)
        json_response = json.loads(response.text)
        if json_response['status'] == 'success':
                return str(json_response['response'])
        else:
            # Respond with random 'confused' message if Error
            print("[!] Failed to Query API")
            return self.confused

    # Return a random 'confused' response to replace errors
    def confused(self):
        excuses = ['I didn\'t catch what you said. Could you repeat it?',
                'I\'m sorry, I didn\'t understand that? Would you mind repeating it?',
                'I\'m sorry, what was that?',
                'Could you say that again, please?',
                'Could you repeat that, please?',
                'I\'m sorry?','Sorry?','Excuse me?',
                'I didn\'t quite understand that.',
                'I beg you pardon?',
                'Say that again.',
                'What?','Huh?','Hmm?','What did you say?',
                'What do you mean?','I don\'t understand.',
                'Excuse me, I didn\'t get it.',
                'Excuse me, can you please repeat it?',
                'Sorry, I did not catch that.','I missed that.',
                'That went right over my head.','Can you please repeat that slowly?',
                'I don\'t get it.','Do you mind explaining it again?',
                'I\'m afraid it is not clear what you saying.',
                'Would you mind clarifying what you said?',
                'I am sorry, but I don\'t follow what you are saying.',
                'I don\'t catch what you said. Sorry.',
                'Say what?','Come again?','I\'m not sure I understand you.',
                'Not sure if I understand.','I\'m not quite getting it.',
                'Can\'t be bothered','I dont care','Whatever','...wait what?']
        return random.choice(excuses)