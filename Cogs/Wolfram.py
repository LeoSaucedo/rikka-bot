"""
Wolfram Module.
Carlos Saucedo, 2020
"""

import discord
from discord.ext import commands
import wolframalpha
import json
from urllib.parse import quote_plus
import aiohttp
import aiofiles


class Wolfram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = json.load(open("json/config.json", "r"))["wolframapi"]

    @commands.command()
    async def wolfimg(self, ctx, *, arg):
        params = {"i": arg, "appid": self.key}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.wolframalpha.com/v1/simple", params=params)as res:
                f = await aiofiles.open("cache/wolfram.jpg", mode="wb")
                await f.write(await res.read())
                image = discord.File("cache/wolfram.jpg",
                                     filename="wolfram.jpg")
                embed = discord.Embed(color=0xff8920)
                embed.set_author(name=arg, icon_url="https://is5-ssl.mzstatic.com/image/thumb/Purple128/v4/19/fd/a8/19fda880-b15a-31a1-958d-32790c4ed5a4/WolframAlpha-AppIcon-0-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/246x0w.jpg",
                                 url=("https://m.wolframalpha.com/input/?i=" + quote_plus(arg)))
                embed.set_footer(text="Wolfram|Alpha, all rights reserved")
                embed.set_image(url="attachment://wolfram.jpg")
                await ctx.send(file=image, embed=embed)

    @commands.command()
    async def wolfram(self, ctx, *, arg):
        params = {"i": arg, "appid": self.key}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.wolframalpha.com/v1/result", params=params) as res:
                response = str(await res.text())
                embed = discord.Embed(description=response, color=0xff8920)
                embed.set_author(name=arg, icon_url="https://is5-ssl.mzstatic.com/image/thumb/Purple128/v4/19/fd/a8/19fda880-b15a-31a1-958d-32790c4ed5a4/WolframAlpha-AppIcon-0-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/246x0w.jpg",
                                 url=("https://m.wolframalpha.com/input/?i=" + quote_plus(arg)))
                embed.set_footer(text="Wolfram|Alpha, all rights reserved")
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wolfram(bot))
