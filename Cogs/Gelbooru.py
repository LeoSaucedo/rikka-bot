import discord
import random
import aiohttp
import json
from discord.ext import commands


async def displayBooruPost(data):
    if data is not None and len(data) > 0:
        embed = discord.Embed(color=0xff28fb)
        embed.set_image(url=data['file_url'])
        embed.title = f"Post ID:{data['id']} | Created:{data['created_at']}" # concat all tags with `, ` inbetween, then concat onto that a start and end `
        tagsFormatted = "".join(('`', "`, `".join(data['tags'].split(' ')), '`'))
        if data['source'] is not None and data['source'] != '':
            embed.description = f"{tagsFormatted}\n[[Gelbooru]](https://gelbooru.com/index.php?page=post&s=view&id={data['id']})[[Source]]({data['source']})"
        else:
            embed.description = f"{tagsFormatted}\n[[Gelbooru]](https://gelbooru.com/index.php?page=post&s=view&id={data['id']})"
        return (1, embed)
    else:
        return (0, 'no data')


async def generateErrorEmbed(msg):
    return discord.Embed(color=0xff0000, title="Error", description=msg)


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

    @commands.command()
    async def gelbooru(self, ctx, *args):
        posts = await fetchJSONData(self.session, 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1')
        if str(args[0]).lower() == 'latest':
            embed = await displayBooruPost(posts[0])
            if embed[0] == 0:
                print(f"[ERROR][Gelbooru] displayBooruPost: empty data for latest post")
                await ctx.send(embed=await generateErrorEmbed('Sorry, there was an unexpected error'))
            elif embed[0] == 1:
                await ctx.send(embed=embed[1])
        if str(args[0]).lower() == 'random':
            post = None
            while post == None:
                # generate number between 0 and latest post ID
                postid = posts[random.randint(0, len(posts) - 1)]
                coro = fetchJSONData(self.session, f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&id={postid}")
                post = await coro
                if post:
                    break
            embed = await displayBooruPost(post[0])
            if embed[0] == 0:
                print(f"[ERROR][Gelbooru] displayBooruPost: empty data for random post (id {postid})")
                await ctx.send(embed=await generateErrorEmbed('Sorry, there was an unexpected error'))
            elif embed[0] == 1:
                await ctx.send(embed=embed[1])
        if str(args[0]).lower() == 'tags':
            search = await fetchJSONData(self.session, 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=' + '+'.join(args[1:]))
            if search:
                post = search[random.randint(0, len(search)-1)]
                embed = await displayBooruPost(post)
                if embed[0] == 0:
                    print(f"[ERROR][Gelbooru] displayBooruPost: empty data for search (id {post['id']})")
                    await ctx.send(embed=await generateErrorEmbed('Sorry, there was an unexpected error'))
                elif embed[0] == 1:
                    await ctx.send(embed=embed[1])
            else:
                await ctx.send(embed=await generateErrorEmbed('Sorry, I couldn\'t find that'))
        if str(args[0]).lower() == 'id':
            if len(args) > 1:
                try:
                    postid = int(args[1])
                except:
                    await ctx.send(embed=await generateErrorEmbed('Please enter a valid post ID!'))
                else:
                    if len(args) > 1 and postid > 0 and postid < int(posts[0]['id']):
                        post = await fetchJSONData(self.session, f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&id={args[1]}")
                        if post:
                            embed = await displayBooruPost(post[0])
                            if embed[0] == 1:
                                await ctx.send(embed=embed[1])
                            else:
                                print(f"[ERROR][Gelbooru] displayBooruPost: empty data for id post (id {args[1]})")
                                await ctx.send(embed=await generateErrorEmbed('Sorry, there was an unexpected error'))
                        else:
                            print(f"[ERROR][Gelbooru] fetchJSONData: error condition for id post (id {args[1]})")
                            await ctx.send(embed=await generateErrorEmbed('Sorry, there was an unexpected error or that post does not exist'))
                    else:
                        await ctx.send(embed=await generateErrorEmbed('Please enter a valid post ID!'))
            else:
                await ctx.send(embed=await generateErrorEmbed('Please enter a post ID!'))
        else:
            await ctx.send(embed=await generateErrorEmbed('Please enter a valid subcommand!'))


def setup(bot):
    bot.add_cog(booru(bot))
