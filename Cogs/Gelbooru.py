import discord
import random
import aiohttp
import json
from discord.ext import commands
from Cogs.Errors import APIError


async def displayBooruPost(data):
    if data is not None and len(data) > 0:
        embed = discord.Embed(color=0xff28fb)
        embed.set_image(url=data['file_url'])
        # concat all tags with `, ` inbetween, then concat onto that a start and end `
        embed.title = f"Post ID:{data['id']} | Created:{data['created_at']}"
        tagsFormatted = "".join(
            ('`', "`, `".join(data['tags'].split(' ')), '`'))
        if data['source'] is not None and data['source'] != '':
            embed.description = f"{tagsFormatted}\n[[Gelbooru]](https://gelbooru.com/index.php?page=post&s=view&id={data['id']})[[Source]]({data['source']})"
        else:
            embed.description = f"{tagsFormatted}\n[[Gelbooru]](https://gelbooru.com/index.php?page=post&s=view&id={data['id']})"
        return (1, embed)
    else:
        return (0, 'no data')


async def fetchJSONData(session, url):
    if url is not None and url != '':
        async with session.get(url) as data:
            if data.status == 200:
                return await data.json()
            else:
                return None


class booru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.validSubCommands = ['id','latest','random','tags']

    @commands.command()
    @commands.is_nsfw()
    async def gelbooru(self, ctx, *args):
        if(len(args) == 0):
            raise InvalidSubcommand('Please enter a subcommand.')
        elif not str(args[0]).lower() in self.validSubCommands:
            raise InvalidSubcommand()
        posts = await fetchJSONData(self.session, 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1')
        if str(args[0]).lower() == 'latest':
            embed = await displayBooruPost(posts[0])
            if embed[0] == 0:
                raise APIError(f"[ERROR][Gelbooru] displayBooruPost: empty data for latest post")
            elif embed[0] == 1:
                await ctx.send(embed=embed[1])
        if str(args[0]).lower() == 'random':
            post = None
            while post == None:
                # generate number between 0 and latest post ID
                maxpostid = int(posts[0]['id']) - 1
                randompostid = random.randint(1, maxpostid)
                coro = fetchJSONData(self.session, f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&id={randompostid}")
                post = await coro
                if post:
                    break
            embed = await displayBooruPost(post[0])
            if embed[0] == 0:
                raise APIError(f"[ERROR][Gelbooru] displayBooruPost: empty data for random post (id {randompostid})")
            elif embed[0] == 1:
                await ctx.send(embed=embed[1])
        if str(args[0]).lower() == 'tags':
            search = await fetchJSONData(self.session, 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=' + '+'.join(args[1:]))
            if search:
                post = search[random.randint(0, len(search)-1)]
                embed = await displayBooruPost(post)
                if embed[0] == 0:
                    raise APIError(f"[ERROR][Gelbooru] displayBooruPost: empty data for search (id {post['id']})")
                elif embed[0] == 1:
                    await ctx.send(embed=embed[1])
            else:
                raise APIError('Sorry, I couldn\'t find that')
        if str(args[0]).lower() == 'id':
            if len(args) > 1:
                try:
                    postid = int(args[1])
                except:
                    raise InvalidPostID()
                else:
                    if len(args) > 1 and postid > 0 and postid < int(posts[0]['id']):
                        post = await fetchJSONData(self.session, f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&id={args[1]}")
                        if post:
                            embed = await displayBooruPost(post[0])
                            if embed[0] == 1:
                                await ctx.send(embed=embed[1])
                            else:
                                raise APIError(f"displayBooruPost: empty data for id post (id {args[1]})")
                        else:
                            raise InvalidPostID(f"[ERROR][Gelbooru] fetchJSONData: error condition for id post (id {args[1]})")
                    else:
                        raise InvalidPostID()
            else:
                raise InvalidPostID()


class InvalidSubcommand(commands.BadArgument):
    """Raised when an invalid subcommand is supplied.
    """

    def __init__(self, message="Invalid subcommand."):
        super().__init__(message)


class InvalidPostID(commands.BadArgument):
    """Raised when the Gelbooru post ID is invalid.
    """

    def __init__(self, message="Invalid post ID."):
        super().__init__(message)


class GelbooruError(APIError):
    """Raised when there is an API error.
    """

    def __init__(self, message="Gelbooru API error."):
        super().__init__(message)


async def setup(bot):
    await bot.add_cog(booru(bot))
