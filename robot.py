"""
Discord Rikka Bot.
Carlos Saucedo, 2018
"""

import discord
import asyncio
import gizoogle
from random import randint

#Auth token
tokenfile = open("auth_token.txt", "r")
rawtoken = tokenfile.read().splitlines()
token = rawtoken[0]

#imagelists
hugsfile = open("hug_gifs.list", "r")
huglist = hugsfile.read().splitlines()
hugcount = len(huglist) - 1 # -1 to compensate for array lengths.

#Instantiates Discord client
client = discord.Client()

@client.event
async def on_message(message):
    #Makes sure bot does not reply to itself
    if message.author == client.user:
        return
    if message.content.startswith(";hello") or message.content.startswith(";hi"):
        """Says hi."""
        msg = "h-hello {0.author.mention}-chan!".format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith(";gizoogle"):
        """Gizoogle!"""
        rawMessage = message.content.replace(";gizoogle ", "")
        translatedMessage = gizoogle.text(rawMessage)
        msg = "{0.author.mention} says: ".format(message) + translatedMessage.format(message)
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
    if message.content.startswith(";hugme"):
        """Hugs the author of the message."""
        msg = "{0.author.mention}: ".format(message) + huglist[randint(0,hugcount)] 
        await client.send_message(message.channel, msg)
    if message.content.startswith(";hug "):
        """Hugs a specified user."""
        msg = "{0.author.mention} hugs {0.mentions[0].mention}! ".format(message) + huglist[randint(0,hugcount)]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
"""
Logs into the server.
"""
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-------")
    print("loaded hugs: " + str(hugcount + 1)) # +1 because humans are not computers.
client.run(token)
