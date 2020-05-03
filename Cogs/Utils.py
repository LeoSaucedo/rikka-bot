import discord
from discord.ext import commands
import random


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sayd(self, ctx, *, arg):
        """Allows the user to send an anonymous message.

        Args:
            ctx (discord.ext.commands.Context): The message context.
            arg (string): The message argument.
        """
        # Remove @everyone and @here
        arg = arg.replace("@everyone", "everyone")
        arg = arg.replace("@here", "here")
        await ctx.send(arg)
        await ctx.message.delete()

    @commands.command()
    async def quickvote(self, ctx, *, arg):
        """Generates a poll for the specified argument.

        Args:
            ctx (discord.ext.commands.Context): The message context.
            arg (string): The message argument.
        """
        # Makes a new vote, and adds a yes and a no reaction option.
        voteEmbed = discord.Embed(color=0x0080c0, description=arg)
        voteEmbed.set_author(
            name="New Vote by " + ctx.author.name + "!", icon_url=ctx.author.avatar_url)
        voteMsg = await ctx.send(embed=voteEmbed)
        await voteMsg.add_reaction("👍")
        await voteMsg.add_reaction("👎")
        await ctx.message.delete()

    @commands.command()
    async def rate(self, ctx, *, arg):
        """Rates the argument out of 10.

        Args:
            ctx (discord.ext.commands.Context): The message context.
            arg (string): The message argument.
        """
        await ctx.send("I rate `"+arg+"` a "+random.randint(0, 10)+"/10!")


def setup(bot):
    bot.add_cog(Utils(bot))
