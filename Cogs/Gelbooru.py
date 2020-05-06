import discord,random,aiohttp,json
from discord.ext import commands

async def displayBooruPost(data):
    if data is not None and len(data) > 0:
        embed = discord.Embed(color=0xff28fb)
        embed.set_image(url = data['file_url'])
        embed.title = f"Post ID:{data['id']} | Created:{data['created_at']}"
        tagsFormatted = "".join(('`',"`, `".join(data['tags'].split(' ')),'`')) # concat all tags with `, ` inbetween, then concat onto that a start and end `
        if data['source'] is not None and data['source'] != '':
            embed.description = f"{tagsFormatted}\n[[Gelbooru]](https://gelbooru.com/index.php?page=post&s=view&id={data['id']})[[Source]]({data['source']})"
        else:
            embed.description = f"{tagsFormatted}\n[[Gelbooru]](https://gelbooru.com/index.php?page=post&s=view&id={data['id']})"
        return (1,embed)
    else:
        return (0,'no data')

async def generateErrorEmbed(msg):
    embed = discord.Embed(color=0xff0000,title="Error",description=msg)

async def fetchJSONData(session,url):
    if url is not None and url != '':
        async with session.get(url) as data:
            if data.status == 200:
                return data.json()
            else:
                return None

class booru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gelbooru(self, ctx, *args):
        session = aiohttp.ClientSession()
        posts = await fetchJSONData(session,'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1')
        if str(args[0]).lower() == 'latest':
            #async with session.get('https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1') as data:
            embed = await displayBooruPost(posts[0])
            if embed[0] == 0:
                print(f"[ERROR][Gelbooru] displayBooruPost: empty data for latest post")
                ctx.send(embed=await generateErrorEmbed('Sorry, there was an unexpected error'))
            elif embed[0] == 1:
                ctx.send(embed=embed[1])
        if str(args[0]).lower() == 'random':
            post == None
            while post == None:
                postid = posts[random.randint(1,posts[0]['id']] #generate number between 0 and latest post ID
                post = await fetchJSONData(session, f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&id={postid}")
                if post:
                    break
            embed = await displayBooruPost(post[0])
            if embed[0] == 0:
                print(f"[ERROR][Gelbooru] displayBooruPost: empty data for random post (id {postid})")
                ctx.send(embed=await generateErrorEmbed('Sorry, there was an unexpected error'))
            elif embed[0] == 1:
                ctx.send(embed=embed[1])
        if str(args[0]).lower() == 'tags':
            search = await fetchJSONData(session, 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=' + '+'.join(args[1:]))
            if search:
                post = search[random.randint(0,len(search)-1)]
                embed = await displayBooruPost(post)
                if embed[0] == 0:
                    print(f"[ERROR][Gelbooru] displayBooruPost: empty data for search (id {post['id']})")
                    ctx.send(embed=await generateErrorEmbed('Sorry, there was an unexpected error'))
                elif embed[0] == 1:
                    ctx.send(embed=embed[1])
            else:
                ctx.send(embed=await generateErrorEmbed('Sorry, I couldn\'t find that'))
        else:
            ctx.send(embed=await generateErrorEmbed('Please enter a valid subcommand!'))
        await session.close()

def setup(bot):
    bot.add_cog(booru(bot))
