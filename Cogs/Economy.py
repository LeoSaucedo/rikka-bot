import discord
from discord.ext import commands
import random
import sqlite3
import datetime


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
  async def leaderboard(self, ctx):
    """Gets the leaderboard."""
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM leaderboard ORDER BY score DESC")
    data = c.fetchall()
    conn.close()
    if(len(data) == 0):
      await ctx.send("There is no one on the leaderboard.")
    else:
      msg = ""
      i = 0
      while(i < 9):
        try:
          user = await self.bot.fetch_user(data[i][1])
          msg += str(i+1) + ": " + "`" + str(user.display_name) + \
              "` - " + str(data[i][2]) + "\n"
          i += 1
        except:
          pass
      embed = discord.Embed(title="Top 10 Globally:",
                            description=msg, color=0x12f202)
      embed.set_author(
          name="Leaderboard", icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/209/money-bag_1f4b0.png")
      await ctx.send(embed=embed)


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


def setup(bot):
  bot.add_cog(Economy(bot))
