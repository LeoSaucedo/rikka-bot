import discord
from discord.ext import commands
import Cogs.Economy as economy
import sqlite3
import re
from random import randint


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
      points = randint(1, 5)
      await ctx.send("Correct! +" + str(points) + " points.")
      await economy.addPoints(str(ctx.guild.id), str(ctx.author.id), points)
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

  @commands.command()
  async def hint(self, ctx):
    """Give a hint to the answer to a trivia question."""
    if ctx.guild.id not in self.currentQuestions:
      await ctx.send("There is no question being asked.")
      return
    else:
      # There is a current question being asked.
      if(economy.getQuantity(str(ctx.author.id), "hint") >= 1):
        # Subtract 5 points from the user's score.
        # await economy.addPoints(ctx.guild.id, ctx.author.id, -1)
        await economy.addItem(str(ctx.author.id), "hint", -1)
        # Send the hint.
        answer = self.currentQuestions[ctx.guild.id]["answer"]
        hint = ""
        for i in range(len(answer)):
          if(str.isalpha(answer[i])):
            hint += "\_ "
          else:
            if(answer[i] == " "):
              hint += " "
            hint += answer[i]
        await ctx.send(hint)
      else:
        # Send a message telling the user they don't have enough points.
        await ctx.send("You don't have enough hints to use this command.")


def setup(bot):
  bot.add_cog(Trivia(bot))
