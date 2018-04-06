"""
Discord Rikka Bot.
Carlos Saucedo, 2018
"""

import discord
import asyncio
import gizoogle
from random import randint
import string
from googletrans import Translator

#Auth token
tokenfile = open("auth_token.txt", "r")
rawtoken = tokenfile.read().splitlines()
token = rawtoken[0]

#lists
hugsfile = open("hug_gifs.list", "r")
huglist = hugsfile.read().splitlines()
hugcount = len(huglist) - 1 # -1 to compensate for array lengths.


#Instances
client = discord.Client()
translator = Translator()

#Discord prefix
prefix = ";"

def command(string):
    #Builds a command out of the given string.
    #Makes you able to change the prefix at any given moment.
    return prefix + string

def getArgument(command, message):
    #Gets the argument text as a string.
    argument = message.content.replace(command + " ", "")
    argument = argument.encode("ascii", "ignore")
    return argument

def getRawArgument(command, message):
    argument = message.content.replace(command + " ", "")
    return argument
    
@client.event
async def on_server_join(server):
    serversConnected = str(len(client.servers))
    print("Joined server " + server.name + "!")
    print("Guilds connected: " + serversConnected)#Returns number of guilds connected to
    await client.change_presence(game=discord.Game(name='on ' + serversConnected + ' servers!')) 
    
@client.event
async def on_message(message):
    """
    Universal commands
    """
    #Makes sure bot does not reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith(command("help")):
        #Returns the README on the GitHub.
        msg = "{0.author.mention} https://discordbots.org/bot/430482288053059584".format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith(command("hello")) or message.content.startswith(command("hi")):
        #Says hi and embeds a gif, mentioning the author of the message.
        msg = "h-hello {0.author.mention}-chan! ".format(message) + 'https://cdn.discordapp.com/attachments/402744318013603840/430592483282386974/image.gif'
        await client.send_message(message.channel, msg)
    
    if message.content.startswith(command("gizoogle")):
        #Gizoogles the given string and returns it.
        translatedMessage = gizoogle.text(getArgument(command("gizoogle"), message))
        msg = "{0.author.mention} says: ".format(message) + translatedMessage.format(message)
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
    
    if message.content.startswith(command("hugme")) or message.content == command("hug"):
        #Hugs the author of the message.
        msg = "{0.author.mention}: ".format(message) + huglist[randint(0,hugcount)] 
        await client.send_message(message.channel, msg)
    
    if message.content.startswith(command("hug ")):
        #Hugs the first user mentioned by the author.
        msg = "{0.author.mention} hugs {0.mentions[0].mention}! ".format(message) + huglist[randint(0,hugcount)]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
    
    if message.content.startswith(command("gay")):
        #no u
        msg = "no u {0.author.mention}".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(command("translate")):
        #Translates the given text into english.
        translatedMessage = translator.translate(getRawArgument(command("translate"), message)).text
        msg = ("{0.author.mention}: translated text - " + translatedMessage).format(message)
        await client.send_message(message.channel, msg)
        
    if message.content.startswith(command("info")):
        #Returns information about the bot.
        msg = ("Hi there! I'm Rikka. This robot was created by Leo. This server's command prefix is: " + prefix + ". To get help, use " + prefix + "help.").format(message)
        await client.send_message(message.channel, msg)
        
    if (len(message.mentions) > 0) and (message.mentions[0] == client.user) and ("help" in message.content):
        msg = ("Hi there! I'm Rikka. This robot was created by Leo. This server's command prefix is: " + prefix + ". To get help, use " + prefix + "help.").format(message)
        await client.send_message(message.channel, msg)

    """
    Administrator Commands.
    """
    if message.channel.permissions_for(message.author).administrator == True:
        if message.content.startswith(command("clear")):
            #Removes a set number of messages.
            number = int(getArgument(command("clear"), message)) + 2
            counter = 0
            async for x in client.logs_from(message.channel, limit=number):
                if counter < number :
                    await client.delete_message(x)
                    counter += 1
                    await asyncio.sleep(0.1)
            msg = "deleted " + str(number - 2) + " messages!".format(string)
            await client.send_message(message.channel, msg)
            
            
    """
    Miscellaneous gifs.
    I know it's ugly, but I'll fix it eventually.
    """
    #Rikka's actions
    if message.content == command("shocked"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430591612637413389/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("smile"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430591877834735617/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("hentai"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593080215994370/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("blush"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593551554969600/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("bdsm"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593796045144064/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("rekt"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594037427470336/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("boop"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594711602987008/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("fuckoff"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594846022041601/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("sanic"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430595068156575756/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("dreamy"):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430595392669745153/image.gif"
        await client.send_message(message.channel, msg)

    #SyCW Commands - By special request.
    if message.server.id == "329383300848418816":
        if message.content == command("assad"):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787413888073728/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("turkey"):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787599343550494/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("bomb"):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787955880230912/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("isis"):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430788102399983617/image.png"
            await client.send_message(message.channel, msg)
        if message.content == command("barrel"):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430788296663367680/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("kurd"):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430789263945105412/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("abuhajaar"):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430804463016476672/image.png"
            await client.send_message(message.channel, msg)
        
"""
Bot login actions
"""
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-------")
    print("loaded hugs: " + str(hugcount + 1)) # +1 because humans are not computers.
    serversConnected = str(len(client.servers))
    print("Guilds connected: " + serversConnected)#Returns number of guilds connected to
    await client.change_presence(game=discord.Game(name='on ' + serversConnected + ' servers!'))
client.run(token) #runs the bot.
