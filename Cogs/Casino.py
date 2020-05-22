"""
Casino Module.
Carlos Saucedo, 2020
"""

import discord
from discord.ext import commands
from random import randint


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def eightball(self, ctx):
        """Gets a message from the eight-ball.

        Args:
            ctx (discord.ext.Context): The message Context.
        """
        responses = [
            "it is certain.",
            "it is decidedly so.",
            "without a doubt.",
            "yes, definitely.",
            "you may rely on it.",
            "you can count on it.",
            "as I see it, yes.",
            "most likely.",
            "outlook good.",
            "yes.",
            "signs point to yes.",
            "absolutely.",
            "reply hazy, try again.",
            "ask again later.",
            "better not tell you now.",
            "cannot predict now.",
            "concentrate and ask again.",
            "don't count on it.",
            "my reply is no.",
            "my sources say no.",
            "outlook not so good.",
            "very doubtful.",
            "chances aren't good."
        ]
        response = ("{0.author.mention}, " +
                    responses[randint(0, len(responses)-1)]).format(ctx.message)
        embed = discord.Embed(color=0x8000ff)
        embed.set_author(
            name="Magic 8-Ball",
            icon_url="https://emojipedia-us.s3.amazonaws.com/thumbs/120/twitter/134/billiards_1f3b1.png",
        )
        embed.add_field(
            name="Prediction:",
            value=response,
            inline=False
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Casino(bot))
