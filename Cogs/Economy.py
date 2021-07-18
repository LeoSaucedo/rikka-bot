import discord
from discord.ext import commands
import random
import sqlite3
import datetime
import re
import json


class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def score(self, ctx):
    """Gets the amount of money you have."""
    if(len(ctx.message.mentions) == 0):
      user = ctx.message.author
    else:
      user = ctx.message.mentions[0]
    await ctx.send("`" + str(user.name) + "`'s score is: " + str(getScore(user.id)))

  @commands.command()
  async def fight(self, ctx):
    """Fights a user and rewards points to the winner."""
    numPlayers = len(ctx.message.mentions)
    vicNum = random.randint(0, numPlayers)
    rewardAmt = random.randint(1, 5)
    if(numPlayers < 1) or (ctx.message.author in ctx.message.mentions):
      msg = '<@!' + str(ctx.message.author.id)+'>' + \
          ", you can't fight yourself! Choose a set of opponents."
      await ctx.send(msg)
    else:
      victor = ctx.message.author if vicNum == numPlayers else ctx.message.mentions[vicNum]
      await addPoints(str(ctx.message.guild.id), str(victor.id), rewardAmt)
      msg = '<@!'+str(victor.id)+'>' + " wins! " + str(rewardAmt)
      msg += " point." if rewardAmt == 1 else " points."
      await ctx.send(msg)
      if numPlayers < 2:
        if not victor == ctx.message.author:
          await addPoints(str(ctx.message.guild.id), str(ctx.message.author.id), rewardAmt * -1)
          loser = str(ctx.message.author.id)
        else:
          await addPoints(str(ctx.message.guild.id), str(ctx.message.mentions[0].id), rewardAmt * -1)
          loser = str(ctx.message.mentions[0].id)
        msg = '<@!' + loser + '>' + \
            ": For your loss, you lose " + str(rewardAmt)
        if rewardAmt == 1:
          msg += " point. Better luck next time."
        else:
          msg += " points. Better luck next time."
        await ctx.send(msg)

  @commands.command()
  async def leaderboard(self, ctx, arg1=None):
    """Gets the leaderboard."""
    if arg1 is None:
      arg1 = 'local'
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()
    if arg1 == 'local':
      guildid = str(ctx.message.guild.id)
      c.execute(
          "SELECT * FROM leaderboard WHERE server=? ORDER BY score DESC", (guildid,))
    elif arg1 == 'global':
      c.execute("SELECT * FROM leaderboard ORDER BY score DESC")
    else:
      await ctx.send(arg1 + " is not a valid option for leaderboard")
      return
    data = c.fetchall()
    conn.close()
    if(len(data) == 0):
      await ctx.send("There is no one on the leaderboard.")
    else:
      msg = ""
      i = 0
      while(i < 9 and i < len(data)):
        try:
          user = '<@!' + str(data[i][1])+'>' if arg1 == 'local' else await self.bot.fetch_user(data[i][1])
          msg += str(i+1) + ": " + user + ': ' + str(data[i][2]) + "\n" if arg1 == 'local' else str(i+1) + ": " + "`" + str(user.display_name) + \
              "` - " + str(data[i][2]) + "\n"
          i += 1
        except:
          pass
      title = "Top 10 Globally:" if arg1 == 'global' else "Top 10 in " + \
          ctx.message.guild.name + ':'
      embed = discord.Embed(title=title,
                            description=msg, color=0x12f202)
      embed.set_author(
          name="Leaderboard", icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/209/money-bag_1f4b0.png")
      await ctx.send(embed=embed)

  @commands.command()
  async def shop(self, ctx):
    """displays shop and allows user to buy items"""
    # displaying initial shop menu with emoji reactions for user input
    emojis = ['🔍', '🎨']
    msg = "Would you like to shop for:\n" + \
        emojis[0] + ": Trivia hints - 5 pts\n" + \
          emojis[1] + ": Custom colors - 20 pts\n"
    embed = discord.Embed(title="Welcome to the shop!",
                          description=msg, color=0x12f202)
    emb = await ctx.send(embed=embed)
    for emoji in emojis:
      await emb.add_reaction(emoji)

    # reaction check function, checks that reaction is made on the display message, by the author, and a valid emoji
    def chk(reaction, user):
      return str(reaction.emoji) in emojis and user == ctx.message.author and reaction.message == emb

    # get reaction from user
    react, user = await self.bot.wait_for('reaction_add', check=chk)

    # message check function, ensures replies to bot are by the author
    def check_message(m):
      return m.author == ctx.message.author

    score = getScore(str(ctx.message.author.id))

    if str(react) == emojis[0]:  # purchasing hints
      await ctx.send('<@!' + str(ctx.message.author.id)+">, Enter the number of hints you would like to purchase.")
      # wait for author to reply
      msg = await self.bot.wait_for('message', check=check_message)
      # check that reply is valid and that user has enough points
      if not msg.content.isnumeric():
        await ctx.send('<@!' + str(ctx.message.author.id)+'>, ' + msg.content + ' is not a valid number of hints.')
        return
      numpurchased = int(msg.content)
      if numpurchased*5 > score:
        await ctx.send('<@!' + str(ctx.message.author.id)+'>, you do not have enough points to purchase ' + str(numpurchased) + ' hints.')
        return
      # subtract points from user, add hints to inventory
      await addPoints(str(ctx.message.guild.id), str(ctx.message.author.id), numpurchased*-5)
      await addItem(str(ctx.message.author.id), "hint", numpurchased)
      await ctx.send('<@!' + str(ctx.message.author.id)+">, you have purchased " + str(numpurchased) + " hints. You now have " + str(score - numpurchased*5) + " points.")
    elif str(react) == emojis[1]:  # purchasing a color
      await ctx.send('<@!' + str(ctx.message.author.id)+">, Enter the hex code of the color you would like to purchase.")
      # function to check that user replied with a hex code

      def isHex(hexcode):
        return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hexcode)
      # wait for author to reply
      msg = await self.bot.wait_for('message', check=check_message)
      # check reply and user points
      if not isHex(msg.content):
        await ctx.send('<@!' + str(ctx.message.author.id)+'>, ' + msg.content + ' is not a valid hex code.')
      elif 20 > score:
        await ctx.send('<@!' + str(ctx.message.author.id)+'>, you do not have enough points to purchase a custom color.')
      else:  # subtract points from user, add color to inventory
        await addPoints(str(ctx.message.guild.id), str(ctx.message.author.id), -20)
        await addItem(str(ctx.message.author.id), msg.content.strip(), 1)
        await ctx.send('<@!' + str(ctx.message.author.id)+'>, your custom color ' + msg.content + ' has been added to your inventory. You now have ' + str(score-20) + ' points.')

  @commands.command()
  async def inv(self, ctx):
    userID = str(ctx.message.author.id)
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()
    c.execute("SELECT inventory FROM inventory WHERE user=?;", (userID,))
    data = c.fetchall()
    conn.close()
    print(data)


async def addPoints(serverID, userID, amount):
  """Adds the specified number of points to the user.

  Args:
      serverID (string): The ID of the server the user is in.
      userID (string): The ID of the user.
      amount (int): The amount of points to add.
  """
  conn = sqlite3.connect("db/database.db")
  c = conn.cursor()

  c.execute("SELECT * FROM leaderboard WHERE user=?;", (userID,))
  if(len(c.fetchall()) == 0):
    # If the user does not exist
    c.execute('''
        INSERT INTO leaderboard VALUES(?, ?, ?, ?);
        ''',
              (serverID, userID, amount, datetime.datetime.now().isoformat()))

  else:
    # User already exists.
    c.execute("SELECT * FROM leaderboard WHERE user=?;", (userID,))
    currentScore = c.fetchone()[2]
    c.execute('''
        UPDATE leaderboard
        SET SCORE=?, SERVER=? WHERE USER=?;
        ''',
              (currentScore+amount, serverID, userID))

  # End the connection
  conn.commit()
  conn.close()


def getScore(userID):
  """
  Returns the score of the user.
  Args:
      userID (string): The ID of the user.
  """
  conn = sqlite3.connect("db/database.db")
  c = conn.cursor()
  c.execute("SELECT score FROM leaderboard WHERE user=?;", (str(userID),))
  score = c.fetchone()
  if(score == None):
    return 0
  else:
    return score[0]


async def addItem(userID, item, quantity):
  """Adds an item to the user's inventory.

  Args:
      userID (string): Discord user ID
      item (string): Name of the item to buy.
      quantity (int): Number of items to buy.
  """
  # Check if the user has an inventory.
  conn = sqlite3.connect("db/database.db")
  c = conn.cursor()
  c.execute("SELECT * FROM inventory WHERE user=?;", (userID,))
  if(len(c.fetchall()) == 0):
    # User does not have an inventory.
    # Create an inventory for the user.
    inventory = {
        item: quantity
    }
    # Add the inventory to the database.
    c.execute("INSERT INTO inventory VALUES(?, ?)",
              (userID, json.dumps(inventory)))
  else:
    # User has an inventory.
    # Add the item to the inventory.
    c.execute("SELECT inventory FROM inventory WHERE user=?", (userID,))
    inventory = json.loads(c.fetchone()[0])
    if(inventory.get(item, 0) <= 0):
      # Remove the item from the inventory.
      inventory.pop(item, None)
    else:
      inventory[item] = inventory.get(item, 0) + quantity
    c.execute("UPDATE inventory SET inventory=? WHERE user=?",
              (json.dumps(inventory), userID))
  conn.commit()
  conn.close()


def getQuantity(userID, item):
  """Returns the number of items in the user's inventory.

  Args:
      userID (string): Discord user ID
      item (string): Name of the item in the inventory.
  """
  conn = sqlite3.connect("db/database.db")
  c = conn.cursor()
  c.execute("SELECT inventory FROM inventory WHERE user=?", (userID,))
  inventory = json.loads(c.fetchone()[0])
  return inventory.get(item, 0)


def setup(bot):
  bot.add_cog(Economy(bot))
