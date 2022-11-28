from random import randint
from typing import Optional, List, Callable

from discord import Embed
from discord.ext import commands
from aiohttp import ClientSession
from discord.ext.commands import Context


class Xkcd(commands.Cog):
    required_response_fields: List[str] = ['year', 'month', 'day', 'alt', 'num']
    theme_color: int = 0x7610ba

    def __init__(self, bot):
        self.bot = bot
        self.formattable_request_url = 'http://xkcd.com/{}/info.0.json'
        self.latest_request_url = 'http://xkcd.com/info.0.json'

    @commands.hybrid_command()
    async def xkcd(self, ctx: Context, args: Optional[str] = None):
        embed: Optional[Embed] = None

        if args is None or args == 'random':
            embed = Xkcd._make_embed(await self.get_specific(randint(0, 100)))
        elif args == 'latest':
            embed = Xkcd._make_embed(await self.get_latest())
        elif Xkcd._try_convert(args) is not None:
            embed = Xkcd._make_embed(await self.get_specific(Xkcd._try_convert(args)))

        if embed is not None and len(embed) > 0:
            return await ctx.send(embed=embed)
        elif embed is None:
            # If embed is Embed.Empty that means json response was not value / invalid input
            return await ctx.send('Sorry, I was unable to retrieve that comic for your. It may not exist. . .')

        return await ctx.send('Sorry, I don\'t understand that command.')

    async def get_specific(self, numeral: int) -> Optional[dict]:
        return await self._fetch_comic(self.formattable_request_url, numeral)

    async def get_latest(self) -> Optional[dict]:
        return await self._fetch_comic(self.latest_request_url)

    async def _fetch_comic(self, url: str, *args) -> Optional[dict]:
        async with ClientSession() as session:
            async with session.get(Xkcd._try_format(url, *args), allow_redirects=True) as response:
                print(response.status)
                if response.status != 200:
                    return {'error': 'Request was made but failed to retrieve data'}
                return await response.json()

    @staticmethod
    def _validate_dict(d: dict) -> bool:
        required_fields = Xkcd.required_response_fields

        # TODO Find a non-(n*m) solution
        for field in required_fields:
            if field not in d.keys():
                return False
        return True

    @staticmethod
    def _make_embed(response: dict) -> Embed:
        if Xkcd._validate_dict(response):
            embed: Embed = Embed(color=Xkcd.theme_color)
            embed.set_image(url=response['img'])
            embed.set_footer(text=response['alt'])

            date = f"{response['month']}/{response['day']}/{response['year']}"
            embed.add_field(name=response['title'], value=date, inline=False)

            return embed
        return Embed.Empty

    @staticmethod
    def _try_format(formattable: str, *args, error_handler: Callable[[Exception], None] = None) -> Optional[str]:
        try:
            return formattable.format(*args)
        except ValueError as ex:
            if error_handler:
                error_handler(ex)
        return None

    @staticmethod
    def _try_convert(n: str) -> Optional[int]:
        try:
            return int(n)
        except ValueError:
            return None


async def setup(bot):
    await bot.add_cog(Xkcd(bot))
