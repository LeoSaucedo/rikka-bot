"""
Discord Rikka-Bot.
Carlos Saucedo, 2020
"""

import discord
from discord.ext import commands
import json
import sqlite3

# The different Cogs supported by Rikka.
# TODO: Add and remove cogs per server.
cogs = [
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


@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)


@bot.event
async def on_ready():
    """Runs when the bot has started.
    """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == "__main__":
    # Add all cogs.
    for cog in cogs:
        bot.load_extension(cog)

    # Load bot token and run bot.
    bot.run(json.load(open("json/config.json", "r"))["token"])
