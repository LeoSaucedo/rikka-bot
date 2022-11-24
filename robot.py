"""
Discord Rikka-Bot.
Carlos Saucedo, 2020
"""

import discord
from discord.ext import commands
import json
import sqlite3
import topgg
import logging
import asyncio

# The different Cogs supported by Rikka.
cogs = [
    "Cogs.Errors",
    "Cogs.Owner",
    "Cogs.Info",
    "Cogs.Utils",
    "Cogs.Wolfram",
    "Cogs.Admin",
    "Cogs.Gelbooru",
    "Cogs.Casino",
    "Cogs.Roles",
    "Cogs.Colors",
    "Cogs.MAL",
    "Cogs.Economy",
    "Cogs.Trivia",
    "Cogs.Xkcd"
]


def get_prefix(bot, message):
  """Returns the prefix of the specified server

  Args:
      bot (discord.ext.AutoShardedBot): The current bot.
      message (discord.Message): The message being sent.

  Returns:
      string: The server's prefix, `;` if no set prefix.
  """
  log_info("Received: " + message.content)
  if not message.guild:
    return ';'
  conn = sqlite3.connect("db/database.db")
  c = conn.cursor()
  c.execute("SELECT prefix FROM prefixes WHERE server=?",
            [message.guild.id])
  prefix = c.fetchone()
  if(len(prefix) == 0):
    log_info(f"No prefix found for server {message.guild.id}")
    return ';'
  else:
    log_info(f"Prefix for server {message.guild.id} is {prefix[0]}")
    return prefix[0]


def log_info(message):
  logging.info(message)
  print(message)


intents = discord.Intents.all()
bot = commands.AutoShardedBot(command_prefix=get_prefix, intents=intents)
botlist = topgg.DBLClient(json.load(open("json/config.json"))["bltoken"]).set_data(bot)
logging.basicConfig(
    filename="bot.log",
    filemode='w',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.ERROR,
    datefmt='%d.%b %Y %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler())


@bot.event
async def on_ready():
  """Runs when the bot has started.
  """
  log_info('Logged in as: '+bot.user.name + ": " + str(bot.user.id))
  log_info("Connected to: " + str(len(bot.guilds)) + " guilds.")
  log_info("Connected to: " + str(len(bot.users)) + " users.")

  # topgg authentication
  try:
    await botlist.post_guild_count()
    log_info("Published server count to topgg.")
  except Exception as e:
    log_info("Failed to post server count to topgg: " + str(e))

  game = discord.Game(name="on " + str(len(bot.guilds))+" guilds!")
  await bot.change_presence(activity=game)


@bot.event
async def on_guild_join(guild):
  log_info("Joined server `" + guild.name + "`!")
  log_info("Connected to: " + str(len(bot.guilds)) + " guilds.")
  log_info("Connected to: " + str(len(bot.users)) + " users.")
  game = discord.Game(name="on " + str(len(bot.guilds))+" guilds!")
  await bot.change_presence(activity=game)


@bot.event
async def on_guild_remove(guild):
  log_info("Left server `" + guild.name + "`.")
  log_info("Connected to: " + str(len(bot.guilds)) + " guilds.")
  log_info("Connected to: " + str(len(bot.users)) + " users.")
  game = discord.Game(name="on " + str(len(bot.guilds))+" guilds!")
  await bot.change_presence(activity=game)


async def main():
  """Loads the cogs and runs the bot.
  """
  for cog in cogs:
    try:
      await bot.load_extension(cog)
      log_info("Loaded " + cog)
    except Exception as e:
      log_info("Failed to load " + cog + ": " + str(e))
  await bot.start(json.load(open("json/config.json"))["token"])

if __name__ == "__main__":
  asyncio.run(main())
