"""
Bot owner commands.
Requires the  bot owner to be called.
Carlos Saucedo, 2020
"""

import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, arg):
        """Reloads a cog.

        Args:
            ctx (discord.ext.Context): The message Context.
            arg (string): The name of the cog to be reloaded.
        """
        try:
            self.bot.reload_extension(arg)
            await ctx.send("Reloaded `" + arg + "` cog.")
        except Exception as e:
            raise e

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, arg):
        """Adds a cog.

        Args:
            ctx (discord.ext.Context): The message Context.
            arg (string): The name of the cog to be reloaded.
        """
        try:
            self.bot.load_extension(arg)
            await ctx.send("Loaded `" + arg + "` cog.")
        except Exception as e:
            raise e

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, arg):
        """Removes a cog.

        Args:
            ctx (discord.ext.Context): The message Context.
            arg (string): The name of the Cog to be reloaded.
        """
        try:
            self.bot.unload_extension(arg)
            await ctx.send("Unloaded `" + arg + "` cog.")
        except Exception as e:
            raise e


def setup(bot):
    bot.add_cog(Owner(bot))
