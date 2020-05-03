"""Under construction dialog.
"""

import discord
from discord.ext import commands
import json

bot = commands.AutoShardedBot(command_prefix=";")


@bot.event
async def on_ready():
    """Runs when the bot has started.
    """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="Under construction..."))

if __name__ == "__main__":

    # Load bot token and run bot.
    with open("json/config.json", "r") as h:
        config = json.load(h)
        bot.run(config["token"])
