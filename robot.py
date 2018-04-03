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
        msg = "h-hello {0.author.mention}-chan! ".format(message) + 'https://cdn.discordapp.com/attachments/402744318013603840/430592483282386974/image.gif'
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
        
    """Miscellaneous gifs"""
    if message.content == ";shocked":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430591612637413389/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";smile":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430591877834735617/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";hentai":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593080215994370/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";blush":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593551554969600/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";bdsm":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593796045144064/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";rekt":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594037427470336/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";boop":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594711602987008/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";fuckoff":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594846022041601/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";sanic":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430595068156575756/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == ";dreamy":
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430595392669745153/image.gif"
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
    print("loaded hugs: " + str(hugcount + 1)) # +1 because humans are not computers.
client.run(token)
