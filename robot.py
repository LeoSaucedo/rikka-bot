"""
Discord Rikka Bot.
Carlos Saucedo, 2018
"""

import discord
import asyncio
import gizoogle

#Auth token
tokenfile = open("auth_token.txt", "r")
rawtoken = tokenfile.read().splitlines()
token = rawtoken[0]

#Instantiates Discord client
client = discord.Client()

@client.event
async def on_message(message):
    #Makes sure bot does not reply to itself
    if message.author == client.user:
        return
    if message.content.startswith(";hello") or message.content.startswith(";hi"):
        """Says hi."""
        msg = "hello {0.author.mention} -chan!".format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith(";gizoogle"):
        """Gizoogle!"""
        rawMessage = message.content.replace(";gizoogle ", "")
        translatedMessage = gizoogle.text(rawMessage)
        msg = translatedMessage.format(message)
        await client.send_message(message.channel, msg)
"""
Logs into the server.
"""
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-------")
client.run(token)
