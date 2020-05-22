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
    "Cogs.Gelbooru"
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


bot = commands.AutoShardedBot(command_prefix=get_prefix)
botlist = dbl.Client(bot, json.load(open("json/config.json"))["bltoken"])
logging.basicConfig(level=logging.INFO)


@bot.event
async def on_ready():
    """Runs when the bot has started.
    """
    logging.info('Logged in as: ', bot.user.name, ": ", bot.user.id)
    logging.info("Connected to: ", len(bot.guilds), " guilds.")
    logging.info("Connected to: ", len(bot.users), " users.")

    # DBL authentication
    try:
        await botlist.post_guild_count()
        logging.info("Published server count to dbl.")
    except Exception as e:
        logging.warning("Failed to post server count to dbl: ", str(e))

    game = discord.Game(name="With " + str(len(bot.users)) +
                        " users, on " + str(len(bot.guilds))+" guilds!")
    await bot.change_presence(activity=game)


@bot.event
async def on_guild_join(guild):
    logging.info("Joined server `", guild.name, "`!")
    logging.info("Connected to: ", len(bot.guilds), " guilds.")
    logging.info("Connected to: ", len(bot.users), " users.")
    game = discord.Game(name="With " + str(len(bot.users)) +
                        " users, on " + str(len(bot.guilds))+" guilds!")
    await bot.change_presence(activity=game)


@bot.event
async def on_guild_remove(guild):
    logging.info("Left server `", guild.name, "`.")
    logging.info("Connected to: ", len(bot.guilds), " guilds.")
    logging.info("Connected to: ", len(bot.users), " users.")
    game = discord.Game(name="With " + str(len(bot.users)) +
                        " users, on " + str(len(bot.guilds))+" guilds!")
    await bot.change_presence(activity=game)


if __name__ == "__main__":
    # Add all cogs.
    for cog in cogs:
        bot.load_extension(cog)

    # Load bot token and run bot.
    bot.run(json.load(open("json/config.json", "r"))["token"])
