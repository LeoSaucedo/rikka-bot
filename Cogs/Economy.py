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
        """Returns the author's score.

        Args:
            ctx (discord.ext.Context): The message Context.
        """
        await ctx.send("Your score is: ", str(await getScore(ctx.author.id)))

    @commands.command()
    async def score(self, ctx, arg):
        user = ctx.message.mentions[0]
        try:
            score = getScore(user.id)
            await ctx.send("`", user.name, "`'s score is: ", score)
        except Exception as e:
            await ctx.send("Could not get score.")
            raise e


async def addPoints(serverID, userID, amount):
    """Adds the specified number of points to the user.

    Args:
        serverID (string): The server the user is in.
        userID (string): The user the server is in.
        amount (int): The amount to add to the user.
    """
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM leaderboard WHERE user=?;", userID)
    if(len(c.fetchall()) == 0):
        # If the user does not exist
        c.execute('''
        INSERT INTO leaderboard VALUES(?, ?, ?, ?);
        ''',
                  (serverID, userID, amount, datetime.datetime.now().isoformat()))

    else:
        # User already exists.
        c.execute("SELECT * FROM leaderboard WHERE user=?;", userID)
        currentScore = c.fetchone()[2]
        c.execute('''
        UPDATE leaderboard
        SET SCORE=? WHERE USER=?;
        ''',
                  (currentScore+amount, userID))

    # End the connection
    conn.commit()
    conn.close()


async def getScore(userID):
    """Returns the score of the user.

    Args:
        userID (int): The user's ID.
    """
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()
    c.execute("SELECT score FROM leaderboard WHERE user=?;", userID)
    user = c.fetchone()
    if(user == None):
        return await 0
    else:
        return await c.fetchone()[0]


def setup(bot):
    bot.add_cog(Economy(bot))
