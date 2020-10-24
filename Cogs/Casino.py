"""
Casino Module.
Carlos Saucedo, 2020
"""

import discord
from discord.ext import commands
from random import randint
import re


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, arg):
        """
        Rolls the specified dice.
        """
        res = "("
        sum = 0
        die = arg.split("d")  # TODO: Modifier support
        if((not die[0].isnumeric()) or (not die[1].isnumeric)):
            raise commands.BadArgument("Invalid dice number.")
            return
        elif(int(die[0]) > 100 or int(die[1]) > 100):
            raise commands.BadArgument("Too large dice number!")
            return
        else:
            for x in range(int(die[0])):
                roll = randint(1, int(die[1]))
                sum += roll
                if(x > 0):
                    res += " + "
                res += str(roll)
            res += ") = " + str(sum)
        embed = discord.Embed(title=arg, description=res, color=0x8000ff)
        embed.set_author(
            name="Dice Roller", icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/209/game-die_1f3b2.png")
        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    async def eightball(self, ctx):
        """
        Gets a message from the eight-ball.
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
        
    @commands.command(name="kekw")
    async def kekw(self, ctx):
        """
        Posts a healthy bit of cringe.
        """
        responses = [
            "dont type to me",
            "idc",
            "ur brainwashed",
            "lib logic",
            "don't care about what your typing",
            "triggered xDDDDDDDDDDD",
            "everyone just attacks me",
            "just a senile old man shouting at the sky",
            "dont care"
        ]
        response = (responses[randint(0, len(responses)-1)]).format(ctx.message)
        embed = discord.Embed(
            color=0x8000ff,
            description=response
        )
        embed.set_author(
            name="kekw",
            icon_url="https://i.imgur.com/KaUqGzV.png"
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Casino(bot))
