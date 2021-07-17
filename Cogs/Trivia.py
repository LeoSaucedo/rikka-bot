import discord
from discord.ext import commands
import Cogs.Economy as economy
import sqlite3


class Trivia(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.currentQuestions = {}

  @commands.command()
  async def ask(self, ctx):
    """Ask a trivia question."""
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM trivia ORDER BY random() LIMIT 1")
    question = c.fetchone()
    conn.close()
    self.currentQuestions[ctx.guild.id] = {
        "question": question[0],
        "answer": question[1]
    }
    await ctx.send(question[0])

  @commands.command(pass_context=True, aliases=['a'])
  async def answer(self, ctx, *, answer):
    """Answer a trivia question."""
    if ctx.guild.id not in self.currentQuestions:
      await ctx.send("There is no question being asked.")
      return
    if answer.lower() == self.currentQuestions[ctx.guild.id]["answer"].lower():
      await ctx.send("Correct! +1 point.")
      await economy.addPoints(str(ctx.guild.id), str(ctx.author.id), 1)
      del self.currentQuestions[ctx.guild.id]
    else:
      await ctx.send("Incorrect!")

  @commands.command()
  async def reveal(self, ctx):
    """Reveal the answer to a trivia question."""
    if ctx.guild.id not in self.currentQuestions:
      await ctx.send("There is no question being asked.")
      return
    await ctx.send(self.currentQuestions[ctx.guild.id]["answer"])
    del self.currentQuestions[ctx.guild.id]


def setup(bot):
  bot.add_cog(Trivia(bot))
