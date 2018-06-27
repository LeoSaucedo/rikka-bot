"""
Discord Rikka Bot.
Carlos Saucedo, 2018
"""
import os
import discord
import Mods.gizoogle as gizoogle
from random import randint
import string
from googletrans import Translator
import dbl
import Mods.CleverApi as CleverApi
from time import sleep
import Mods.trivia as trivia
import Mods.triviaScore as triviaScore
from discord.emoji import Emoji
import Mods.EightBall as EightBall
import Mods.economy as econ
import Mods.marriage as marriage

# Directory stuff
root_dir = os.path.dirname(__file__)

# Auth tokens
tokenfile = open("auth_token.txt", "r")
rawtoken = tokenfile.read().splitlines()
token = rawtoken[0]

bltokenfile = open("dbl_token.txt", "r")
rawbltoken = bltokenfile.read().splitlines()
bltoken = rawbltoken[0]
shardCount = 1  # Keeping it simple with 1 for now.

clevertokenfile = open("clever_token.txt", "r")
rawclevertoken = clevertokenfile.read().splitlines()
userapi = rawclevertoken[0]
keyapi = rawclevertoken[1]

# Cleverbot
try:
    clever = CleverApi.Bot(userapi, keyapi)
except Exception as e:
    print("Failed to instantiate CleverBot.")

# lists
hug_relPath = "Lists/hug_gifs.list"
hug_absPath = os.path.join(root_dir, hug_relPath)
hugsfile = open(hug_absPath, "r")
huglist = hugsfile.read().splitlines()
hugCount = len(huglist)
hugsfile.close()

ramsay_relPath = "Lists/ramsay.list"
ramsay_absPath = os.path.join(root_dir, ramsay_relPath)
ramsayfile = open(ramsay_absPath)
ramsaylist = ramsayfile.read().splitlines()
ramsayCount = len(ramsaylist)
ramsayfile.close()

sfwinsult_relPath = "Lists/sfwinsults.list"
sfwinsult_absPath = os.path.join(root_dir, sfwinsult_relPath)
insultfile = open(sfwinsult_absPath)
insultlist = insultfile.read().splitlines()
insultCount = len(insultlist)
insultfile.close()

nsfwinsult_relPath = "Lists/nsfwinsults.list"
nsfwinsult_absPath = os.path.join(root_dir, nsfwinsult_relPath)
nsfwinsultfile = open(nsfwinsult_absPath)
nsfwinsultlist = nsfwinsultfile.read().splitlines()
nsfwInsultCount = len(nsfwinsultlist)
nsfwinsultfile.close()

# Instances
client = discord.Client()
translator = Translator()
botlist = dbl.Client(client, bltoken)

# Prefix things
defaultPrefix = ";"

# Trivia instantiation
question_relPath = "Lists/trivia_questions.list"
questionPath = os.path.join(root_dir, question_relPath)
answer_relPath = "Lists/trivia_answers.list"
answerPath = os.path.join(root_dir, answer_relPath)
trivia = trivia.triviaGame(questionPath, answerPath)
isSent = False

# Eight ball instantiation
eight = EightBall.eightBallGenerator()

def getServerPrefix(guild):
    # Returns the server prefix.
    # If there is no server prefix set, it returns the defaultPrefix.
    prefixFile = open("server_prefixes.txt", "r+")
    prefixList = prefixFile.read().splitlines()
    prefixFile.close()
    serverInList = False
    for line in prefixList:
        splitLine = line.split()
        if guild.id == int(splitLine[0]):
            serverInList = True
            return splitLine[1]
    if serverInList == False:
        # If server does not have default prefix set
        return defaultPrefix


def command(string, message):
    # Builds a command out of the given string.
    serverPrefix = getServerPrefix(message.channel.guild)
    return serverPrefix + string


def getArgument(command, message):
    # Gets the argument text as a string.
    argument = message.content.replace(command + " ", "")
    argument = argument.encode("ascii", "ignore")
    return argument


def getRawArgument(command, message):
    # Gets the raw argument, without being formatted.
    argument = message.content.replace(command + " ", "")
    return argument
    
@client.event
async def on_guild_join(guild):
    serversConnected = str(len(client.guilds))
    usersConnected = str(len(client.users))
    print("Joined server " + guild.name + "!")
    print("Guilds connected: " + serversConnected)  # Returns number of guilds connected to
    print("Users connected: "+ usersConnected)
    game = discord.Game(name='with ' + usersConnected + ' users, on ' + serversConnected + ' servers!')
    await client.change_presence(activity=game)
    try:
        await botlist.post_server_count()
        print("Successfully published server count to dbl.")
    except Exception as e:
        print("Failed to post server count to tbl.")

    
@client.event
async def on_guild_remove(guild):
    serversConnected = str(len(client.guilds))
    usersConnected = str(len(client.users))
    print("Guilds connected: " + serversConnected)  # Returns number of guilds connected to
    print("Users connected: "+ usersConnected)
    game = discord.Game(name='with ' + usersConnected + ' users, on ' + serversConnected + ' servers!')
    await client.change_presence(activity=game)
    try:
        await botlist.post_server_count()
        print("Successfully published server count to dbl.")
    except Exception as e:
        print("Failed to post server count to tbl.") 

    
@client.event
async def on_message(message):
    """
    Universal commands
    """
    if message.author == client.user:
        # Makes sure bot does not reply to itself
        return
    
    elif message.author.bot == True:
        # Makes sure bot does not reply to another bot.
        return
    
    elif str(message.channel).startswith("Direct Message"):
        # If message is direct message.
        msg = "Hi there! Here is my commands list. https://discordbots.org/bot/430482288053059584".format(message)
        await message.channel.send(msg)
    
    elif message.content.startswith(command("help", message)):
        # Returns the README on the GitHub.
        msg = "{0.author.mention} https://discordbots.org/bot/430482288053059584".format(message)
        await message.channel.send(msg)
    
    elif message.content == command("hi", message) or message.content == command("hello", message):
        # Says hi and embeds a gif, mentioning the author of the message.
        msg = "h-hello {0.author.mention}-chan! ".format(message) + 'https://cdn.discordapp.com/attachments/402744318013603840/430592483282386974/image.gif'
        await message.channel.send(msg)
    
    elif message.content.startswith(command("gizoogle", message)):
        # Gizoogles the given string and returns it.
        translatedMessage = gizoogle.text(getArgument(command("gizoogle", message), message))
        msg = "{0.author.mention} says: ".format(message) + translatedMessage.format(message)
        await message.channel.send(msg)
        await message.delete()
    
    elif message.content.startswith(command("hugme", message)) or message.content == command("hug", message):
        # Hugs the author of the message.
        msg = "{0.author.mention}: ".format(message) + huglist[randint(0, hugCount - 1)] 
        await message.channel.send(msg)
    
    elif message.content.startswith(command("hug ", message)):
        # Hugs the first user mentioned by the author.
        msg = "{0.author.mention} hugs {0.mentions[0].mention}! ".format(message) + huglist[randint(0, hugCount - 1)]
        await message.channel.send(msg)
        await message.delete()
        
    elif message.content.startswith(command("ramsay", message)):
        # Replies with a random Gordon Ramsay quote.
        msg = ramsaylist[randint(0, ramsayCount - 1)]
        await message.channel.send(msg)
    
    elif message.content.startswith(command("gay", message)):
        # no u
        msg = "no u {0.author.mention}".format(message)
        await message.channel.send(msg)

    elif message.content.startswith(command("translate", message)):
        # Translates the given text into english.
        translatedMessage = translator.translate(getRawArgument(command("translate", message), message)).text
        msg = ("{0.author.mention}: translated text - " + translatedMessage).format(message)
        await message.channel.send(msg)
        
    elif message.content.startswith(command("clever", message)):
        # Returns CleverBot's response.
        async with message.channel.typing():
            query = getRawArgument(command("clever", message), message)
            try:
                msg = clever.ask(query)
            except Exception as cleverBotException:
                msg = "cleverbot.io API error. Try again later."
            await message.channel.send(msg)
        
    elif message.content.startswith(command("info", message)):
        # Returns information about the bot.
        msg = ("Hi there! I'm Rikka. This robot was created by Leo. This server's command Prefix is: " + getServerPrefix(message.channel.guild) + ". To get help, use " + getServerPrefix(message.channel.guild) + "help.").format(message)
        await message.channel.send(msg)
        
    elif (len(message.mentions) > 0) and (message.mentions[0] == client.user) and ("help" in message.content):
        # Returns information about the bot.
        msg = ("Hi there! I'm Rikka. This robot was created by Leo. This server's command Prefix is: " + getServerPrefix(message.channel.guild) + ". To get help, use " + getServerPrefix(message.channel.guild) + "help.").format(message)
        await message.channel.send(msg)
        
    elif message.content.startswith(command("donate", message)) or message.content.startswith(command("patreon", message)):
        msg = ("Help my programmer out, become a patron today! https://www.patreon.com/LeoSaucedo").format(message)
        await message.channel.send(msg)
        
    elif message.content.startswith(command("vote", message)):
        msg = "Vote for me to take over the world! https://discordbots.org/bot/430482288053059584/vote".format(message)
        await message.channel.send(msg)

    elif message.content.startswith(command("insult ", message)):
        # Says a random insult using an insult generator
        if message.channel.is_nsfw():
            # If the channel is isfw.
            msg = "{0.author.mention} calls {0.mentions[0].mention} ".format(message) + nsfwinsultlist[randint(0, nsfwInsultCount - 1)] + "!"
        else:
            msg = "{0.author.mention} calls {0.mentions[0].mention} ".format(message) + insultlist[randint(0, insultCount - 1)] + "!"
        await message.channel.send(msg)
        await message.delete()
        
    elif message.content.startswith(command("quickvote", message)):
        # Makes a new vote, and adds a yes and a no reaction option.
        voteText = getRawArgument(command("quickvote", message), message)
        voteEmbed = discord.Embed(color=0x0080c0, description=voteText)
        voteEmbed.set_author(name="New Vote by " + message.author.name + "!", icon_url=message.author.avatar_url)
        voteMsg = await message.channel.send(embed=voteEmbed)
        await voteMsg.add_reaction("👍")
        await voteMsg.add_reaction("👎")
        await message.delete()
        
    elif message.content.startswith(command("rate", message)):
        # Rates a certain user or thing.
        thingToRate = getRawArgument(command("rate", message), message)
        rateScore = randint(0, 10)
        msg = ("I rate " + thingToRate + " a **" + str(rateScore) + "/10**.").format(message)
        await message.channel.send(msg)
        
    elif message.content.startswith(command("suggest ", message)) or message.content.startswith(command("suggestion ", message)):
        # Adds ability to suggest new features.
        suggestion = getRawArgument(command("suggest", message), message)
        suggestionsFile = open("suggestions.txt", "a+")
        suggestionsFile.write(suggestion + "\n")
        msg = "{0.author.mention} Added your suggestion! It will be processed and may be added soon! Thanks for the help!".format(message)
        await message.channel.send(msg)
        
    elif message.content.startswith(command("fight ", message)):
        numberOfPlayers = len(message.mentions)
        victorNumber = randint(0, numberOfPlayers)
        rewardAmount = randint(1,5)
        authorLoses = False
        if (numberOfPlayers < 1) or (message.author in message.mentions):
            msg = "{0.author.mention}, you can't fight yourself! Choose a set of opponents.".format(message)
            await message.channel.send(msg)
        else:
            if victorNumber == numberOfPlayers:
                victor = message.author
            else:
                victor = message.mentions[victorNumber]
                if numberOfPlayers < 2:
                    trivia.subtractPoints(message.guild.id, message.author.id, rewardAmount)
                    authorLoses = True
            #TODO embed this and make it pretty.
            trivia.addPoints(message.guild.id, victor.id, rewardAmount)
            msg = ("{0.mention} wins! +"+str(rewardAmount)+" points.").format(victor)
            await message.channel.send(msg)
            if authorLoses == True:
                msg = ("{0.author.mention}: For your loss, you lose "+str(rewardAmount)+" points. Better luck next time!").format(message)
                await message.channel.send(msg)
            
        
    elif message.content == command("flip", message):
        """
        "Casino" Commands
        """
        # User is flipping a coin.
        coinResult = randint(0, 1)
        if coinResult == 0:
            msg = "{0.author.mention} flips a coin. It lands on heads.".format(message)
        elif coinResult == 1:
            msg = "{0.author.mention} flips a coin. It lands on tails.".format(message)
        await message.channel.send(msg)
        
    elif message.content == command("roll", message):
        # User rolls a die.
        diceResult = randint(1, 6)
        msg = ("{0.author.mention} rolls a die. It lands on " + str(diceResult) + ".").format(message)
        await message.channel.send(msg)
    
    elif message.content.startswith(command("8ball", message)):
        result = eight.getAnswer()
        ballText = ("{0.author.mention}, " + result).format(message)
        ballEmbed = discord.Embed(color=0x8000ff)
        ballEmbed.set_author(name="Magic 8-Ball", icon_url="https://emojipedia-us.s3.amazonaws.com/thumbs/120/twitter/134/billiards_1f3b1.png")
        ballEmbed.add_field(name="Prediction:", value=ballText, inline=False)
        await message.channel.send(embed=ballEmbed)
            
    elif message.content == command("collect daily", message):
        """
        Economy commands.
        """
        userID = message.author.id
        serverID = message.guild.id
        if econ.hasCollectedToday(userID):
            msg = "{0.author.mention}, you have already collected today. Try again tomorrow!".format(message)
            await message.channel.send(msg)
        else:
            pointsToAdd = randint(1,25)
            trivia.addPoints(serverID, userID, pointsToAdd)
            econ.setCollectionDate(userID)
            msg = ("{0.author.mention}, your daily points are "+str(pointsToAdd)+"!").format(message)
            await message.channel.send(msg)
            
    elif message.content == command("leaderboard global", message):
        scoreList = ""
        globalScores = trivia.getGlobalLeaderboard()
        if len(globalScores) < 10:
            place = 1
            for score in globalScores:
                user = client.get_user(int(score.getUser()))
                if user != None:
                    score = score.getScore()
                    scoreList = scoreList + (str(place) + ": "+ user.name + " with "+score + " points!\n")
                    place = place + 1
        else:
            i = 0
            place = 1
            while i < 10:
                user = client.get_user(int(globalScores[i].getUser()))
                if user != None:
                    score = globalScores[i].getScore()
                    scoreList = scoreList + (str(place) + ": "+ user.name + " with "+score + " points!\n")
                    place = place + 1
                i = i + 1
            
        scoreEmbed = discord.Embed(title= "Global Leaderboard", color=0x107c02, description=scoreList)
        await message.channel.send(embed=scoreEmbed)
        
    elif message.content == command("leaderboard local", message):
        scoreList = ""
        localScores = trivia.getLocalLeaderboard(message.guild.id)
        if len(localScores) < 10:
            place = 1
            for score in localScores:
                user = client.get_user(int(score.getUser())).name
                if user != None:
                    score = score.getScore()
                    scoreList = scoreList + ("".join((str(place),": ",user.name," with ",score," points!\n")))
                    place = place + 1
        else:
            i = 0
            place = 1
            while i < 10:
                user = client.get_user(int(localScores[i].getUser()))
                if user != None:
                    score = localScores[i].getScore()
                    scoreList = scoreList + ("".join((str(place),": ",user.name," with ",score," points!\n")))
                    place = place + 1
                i = i + 1
        scoreEmbed = discord.Embed(title= "Local Leaderboard", color=0x107c02, description=scoreList)
        await message.channel.send(embed=scoreEmbed)
    
    elif message.content == command("trivia", message):
        """
        Trivia commands.
        """
        prefix = getServerPrefix(message.guild)
        msg = "To get a question, type " + prefix + "ask. To attempt an answer, type " + prefix + "a (attempt). To reveal the answer, type " + prefix + "reveal."
        await message.channel.send(msg)
        msg = "If you believe a question is unfair, type " + prefix + "flag. It will be reviewed by our developers, and removed if appropriate."
        await message.channel.send(msg)
        msg = "To check your score, type " + prefix + "score. Good luck!"
        await message.channel.send(msg)
        
    elif message.content.startswith(command("ask", message)):
        # Returns a randomly generated question.
        msg = trivia.getQuestion(message.guild.id)
        await message.channel.send(msg)
        global isSent
        trivia.setSent(message.guild.id, True)
        
    elif message.content.startswith(command("reveal", message)):
        if trivia.getSent(message.guild.id) == True:
            msg = trivia.getAnswer(message.guild.id)
            await message.channel.send(msg)
            trivia.setSent(message.guild.id, False)
        elif trivia.getSent(message.guild.id) == False:
            msg = "You haven't asked a question yet!"
            await message.channel.send(msg)
            
    elif message.content.startswith(command("flag", message)):
        trivia.flag()
        msg = "Flagged the question! Sorry about that."
        await message.channel.send(msg)
        
    elif message.content.startswith(command("score", message)):
        msg = ("{0.author.mention}, your score is " + str(trivia.getScore(message.author.id))).format(message)
        await message.channel.send(msg)
        
    elif message.content.startswith(command("a", message) + " "):
        # The user is attempting to answer the question.
        attempt = getRawArgument(command("a", message), message)
        if trivia.getSent(message.guild.id) == True:
            # If the question is sent and the answer has not yet been revealed.
            if trivia.format(attempt) == trivia.format(trivia.getAnswer(message.guild.id)):
                # If the answer is correct.
                reward = randint(1,20)
                msg = ("{0.author.mention}, correct! The answer is " + trivia.getAnswer(message.guild.id)+". +"+ str(reward) +" points!").format(message)
                await message.channel.send(msg)
                trivia.addPoints(message.guild.id, message.author.id, reward)
                trivia.setSent(message.guild.id, False)
        else:
            msg = "You haven't gotten a question yet!"
            await message.channel.send(msg)
            
    elif message.content.startswith(command("marriage", message)):
        """
        Marriage RP commands.
        """
        if message.content.startswith(command("marriage propose", message)):
            """
            User is proposing to another user.
            """
            proposer = message.author
            proposee = message.mentions[0]
            
            
            
            
    elif message.content.startswith(command("board", message)):
        """
        Board enable command.
        """
        if message.channel.permissions_for(message.author).manage_channels == True:
            if getRawArgument(command("board", message), message) == "enable":
                if message.channel.permissions_for(message.author).manage_channels == True:
                    await message.guild.create_text_channel('board')
                    msg = "Created board channel! You might want to change the channel permissions/category."
                    await message.channel.send(msg)
                else:
                    msg = "Insufficient permissions."
                    await message.channel.send(msg)
                
    elif message.content.startswith(command("kick", message)):
        """
        Kick command.
        """
        if message.channel.permissions_for(message.author).kick_members == True:
            user = message.mentions[0]
            try:
                await message.guild.kick(user)
                msg = "Kicked " + user.name + "!"
                await message.channel.send(msg)
            except exception as e:
                msg = "Failed to kick user."
                await message.channel.send(msg)
        else:
            msg = "Insufficient permissions."
            await message.channel.send(msg)

    elif message.content.startswith(command("ban", message)):
        """
        Ban command.
        """
        if message.channel.permissions_for(message.author).ban_members == True:
            user = message.mentions[0]
            try:
                await message.guild.ban(user)
                msg = "Banned " + user.name + "!"
                await message.channel.send(msg)
            except:
                msg = "Failed to ban user."
                await message.channel.send(msg)
                
        else:
            msg = "Insufficient permissions."
            await message.channel.send(msg)
    
    elif message.channel.permissions_for(message.author).manage_messages == True:
        """
        Moderator commands.
        """
        if message.content.startswith(command("clear", message)):
            # Clears a specified number of messages.
            
            if(len(message.mentions) > 0):
                #Clear command contains a mention.
                number = 0
                messages = []
                async for msg in message.channel.history():
                    if msg.author == message.mentions[0]:
                        messages.append(msg)
                        number = number+1
                if(len(messages) < 1):
                   msg = "Could not find any messages from the specified user."
                   await message.channel.send(msg)
                else:
                    await message.channel.delete_messages(messages)
                    msg = "deleted " + str(number) + " messages!".format(message)
                    deletemsg = await message.channel.send(msg)
                    sleep(5)
                    await deletemsg.delete()
                
            else:
                number = int(getArgument(command("clear", message), message))
                await message.channel.purge(limit=(number + 1), bulk=True)
                msg = "deleted " + str(number) + " messages!".format(string)
                deletemsg = await message.channel.send(msg)
                sleep(5)
                await deletemsg.delete()
            
        elif message.content.startswith(command("mute", message)):
            if len(message.mentions) > 0:
                sinner = message.mentions[0]
                await message.channel.set_permissions(sinner, send_messages=False)
                msg = "Muted {0.mentions[0].mention}!".format(message)
                await message.channel.send(msg)
            else:
                msg = "You must specify a user."
                await message.channel.send(msg)
            
        elif message.content.startswith(command("unmute", message)):
            if len(message.mentions) > 0:
                sinner = message.mentions[0]
                await message.channel.set_permissions(sinner, send_messages=True)
                msg = "Unmuted {0.mentions[0].mention}!".format(message)
                await message.channel.send(msg)
            else:
                msg = "You must specify a user."
                await message.channel.send(msg)
    
    if message.channel.permissions_for(message.author).administrator == True:
        """
        Administrator Commands.
        """
        if message.content.startswith(command("prefix", message)):
            # Changes the prefix to the specified string.
            prefixFile = open("server_prefixes.txt")
            prefixList = prefixFile.read().splitlines()
            prefixFile.close()
            serverInList = False  # Gotta initialize the variable
            newPrefix = getRawArgument(command("prefix", message), message)
            index = 0
            for line in prefixList:
                splitLine = line.split()
                if(message.channel.guild.id == int(splitLine[0])):
                    # If the server already has a custom prefix set
                    serverInList = True
                    prefixFile = open("server_prefixes.txt", "w+")
                    prefixList[index] = (str(message.channel.guild.id) + " " + newPrefix)
                    prefixFile.write("\n".join(prefixList))
                    prefixFile.close()
                    msg = ("Changed server prefix to " + newPrefix + " !").format(message)
                    await message.channel.send(msg)
                index = index + 1
            if serverInList == False:
                # If the server does not already have a custom prefix set
                prefixFile = open("server_prefixes.txt", "a+")
                prefixFile.write("\n" + str(message.channel.guild.id) + " " + newPrefix)  # Adds line to prefixlist
                prefixFile.close()
                msg = ("Set server prefix to " + newPrefix + " !").format(message)
                await message.channel.send(msg)
                
        """
        Misc gif commands.
        """
    if message.content == command("shocked", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430591612637413389/image.gif"
        await message.channel.send(msg)
    elif message.content == command("smile", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430591877834735617/image.gif"
        await message.channel.send(msg)
    elif message.content == command("hentai", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593080215994370/image.gif"
        await message.channel.send(msg)
    elif message.content == command("blush", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593551554969600/image.gif"
        await message.channel.send(msg)
    elif message.content == command("bdsm", message):
        msg = "http://i.imgur.com/dI4zJwk.gif"
        await message.channel.send(msg)
    elif message.content == command("rekt", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594037427470336/image.gif"
        await message.channel.send(msg)
    elif message.content == command("boop", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594711602987008/image.gif"
        await message.channel.send(msg)
    elif message.content == command("fuckoff", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594846022041601/image.gif"
        await message.channel.send(msg)
    elif message.content == command("sanic", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430595068156575756/image.gif"
        await message.channel.send(msg)
    elif message.content == command("dreamy", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430595392669745153/image.gif"
        await message.channel.send(msg)
    elif message.content == command("waifu", message):
        msg = "https://i.pinimg.com/originals/bd/9a/a4/bd9aa46572e180ec6df08119429a1e81.jpg"
        await message.channel.send(msg)
    elif message.content == command("trash", message):
        msg = "https://media1.tenor.com/images/29307201260fb755e7ff9fec21f22c95/tenor.gif?itemid=8811727"
        await message.channel.send(msg)
    elif message.content == command("kys", message):
        msg = "https://imgur.com/YfYwzcN"
        await message.channel.send(msg)
    elif message.content == command("ping", message):
        msg = "Why did you feel the need to ping everyone? What could possibly be so important that you decided to alert everyone on this god-forsaken server to what you had to say? Did you get a girlfriend? Lose your virginity? Did you become president of the goddamn world? Is that why you had to ping us? I bet you're so proud of yourself, snickering to yourself as you watch the chaos unfold after your ping. You think you're so funny, interrupting everyone's day with your asinine messages. But guess what, you're pathetic. The only way you were able to get someone's attention is by shoving down your sad excuse of a thought down everyone's throat, shattering their focus with that loud PING! I wonder how many people you've killed by doing this. Maybe someone was driving and the ping caused them to lose control and crash. Maybe a surgeon was performing open heart surgery and was jolted by the obnoxious pinging noise of a new notification. Can you live with yourself knowing how many lives you've cost by thinking you had something important to say? I hope you're happy with yourself."
        await message.channel.send(msg)

    # SyCW Commands - By special request.
    elif message.channel.guild.id == 329383300848418816:
        if message.content == command("assad", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787413888073728/image.jpg"
            await message.channel.send(msg)
        elif message.content == command("turkey", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787599343550494/image.jpg"
            await message.channel.send(msg)
        elif message.content == command("bomb", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787955880230912/image.jpg"
            await message.channel.send(msg)
        elif message.content == command("isis", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430788102399983617/image.png"
            await message.channel.send(msg)
        elif message.content == command("barrel", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430788296663367680/image.jpg"
            await message.channel.send(msg)
        elif message.content == command("kurd", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430789263945105412/image.jpg"
            await message.channel.send(msg)
        elif message.content == command("abuhajaar", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430804463016476672/image.png"
            await message.channel.send(msg)

        
"""
Bot login actions
"""


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-------")
    print("loaded hugs: " + str(hugCount))
    print("loaded Ramsay quotes: " + str(ramsayCount))
    print("Loaded questions: " + str(trivia.getQuestionCount()))
    serversConnected = len(client.guilds)
    usersConnected = len(client.users)
    print("Guilds connected: " + str(serversConnected))  # Returns number of guilds connected to
    print("Shards connected: "+ str(shardCount))
    print("Users connected: " + str(usersConnected))
    game = discord.Game(name='with ' + str(usersConnected) + ' users, on '+str(serversConnected)+" servers!")
    await client.change_presence(activity=game)
    try:
        await botlist.post_server_count()
        print("Successfully published server count to dbl.")
    except Exception as e:
        print("Failed to post server count to tbl.")
    
while True:
    client.run(token)  # runs the bot.
