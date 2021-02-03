"""
Discord Rikka-Bot.
Carlos Saucedo, 2020
"""

import discord
from discord.ext import commands
import json
import sqlite3
import dbl
import logging

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
    "Cogs.MAL"
]


def get_prefix(bot, message):
    """Returns the prefix of the specified server

    Args:
        bot (discord.ext.AutoShardedBot): The current bot.
        message (discord.Message): The message being sent.

    Returns:
        string: The server's prefix, `;` if no set prefix.
    """
    if not message.guild:
        return ';'
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()
    c.execute("SELECT prefix FROM prefixes WHERE server=?",
              (str(message.guild.id),))
    prefix = c.fetchall()
    if(len(prefix) == 0):
        return ';'
    else:
        return prefix[0]


def log_info(message):
    logging.info(message)
    print(message)


bot = commands.AutoShardedBot(command_prefix=get_prefix)
botlist = dbl.Client(bot, json.load(open("json/config.json"))["bltoken"])
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

    # DBL authentication
    try:
        await botlist.post_guild_count()
        log_info("Published server count to dbl.")
    except Exception as e:
        log_info("Failed to post server count to dbl: " + str(e))

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


if __name__ == "__main__":
    # Add all cogs.
    for cog in cogs:
        bot.load_extension(cog)

    while True:
        # Load bot token and run bot.
        bot.run(json.load(open("json/config.json", "r"))["token"])
