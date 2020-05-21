import discord
import random
import aiohttp
import json
import datetime
from discord.ext import commands
from time import sleep
from Cogs.Errors import APIError
baseAPIURL = 'https://api.jikan.moe/v3'
with open('json/indicators.json', 'r') as h:
    regionalindicators = json.load(h)
menus = {}
session = aiohttp.ClientSession()
lastRequest = datetime.datetime.utcnow().timestamp()


async def generateErrorEmbed(msg):
    embed = discord.Embed(color=0xff0000, title="Error", description=msg)


async def fetchJSONData(session, url):
    if url is not None and url != '':
        async with session.get(url) as data:
            if data.status == 200:
                return await data.json()
            else:
                raise JikanError(
                    f'[ERROR][MAL] fetchJSONData - code {data.status} when fetching URL \'{url}\'')
                return None


async def RLRequest(session, url):  # rate-limits requests to jikan endpoint
    global lastRequest
    while lastRequest == 0:
        sleep(0.5)
    time = datetime.datetime.utcnow().timestamp()
    lr = lastRequest + 2
    lastRequest = 0
    if time < lr:
        sleep(lr - time)
    response = await fetchJSONData(session, url)
    lastRequest = datetime.datetime.utcnow().timestamp()
    return response


async def checkExists(property, dict):
    if str(property) in dict:
        if dict[str(property)] is not None and dict[str(property)] != '' and dict[str(property)] != 'null':
            return True
        else:
            return False
    else:
        return False


async def fetchItem(session, id):
    # checking content type
    data = None
    if id.startswith('A/'):
        type = 'anime'
        data = await RLRequest(session, f'{baseAPIURL}/anime/{id[2:]}/')
    elif id.startswith('M/'):
        type = 'manga'
        data = await RLRequest(session, f'{baseAPIURL}/manga/{id[2:]}/')
    else:  # assume anime
        type = 'anime'
        data = await RLRequest(session, f'{baseAPIURL}/anime/{id}/')
    return data


async def formatItem(session, data):
    if data:
        embed = discord.Embed(color=0x2e51a2)
        if await checkExists('title', data):
            if await checkExists('type', data):
                embed.title = f"[{data['mal_id']}][{data['type']}][{data['title']}]"
            else:
                embed.title = f"[{data['mal_id']}][{data['title']}]"
        elif await checkExists('title_english', data):
            if await checkExists('type', data):
                embed.title = f"[{data['mal_id']}][{data['type']}][{data['title_english']}]"
            else:
                embed.title = f"[{data['mal_id']}][{data['title_english']}]"
        if await checkExists('synopsis', data):
            if len(data['synopsis']) > 600:
                synopsis = data['synopsis'][0:599]
            else:
                synopsis = data['synopsis']
            embed.description = f'[[url]](https://myanimelist.net/anime/{data["mal_id"]})\n```\n{synopsis}\n```'
        if await checkExists('image_url', data):
            embed.set_thumbnail(url=data['image_url'])
        if await checkExists('genres', data):
            if len(data['genres']) > 0:
                name = 'Genre'
                arrGenres = []
                if len(data['genres']) > 1:
                    name = 'Genres'
                for genre in data['genres']:
                    if await checkExists('url', genre):
                        arrGenres.append(
                            f"[{genre['name']}](https://myanimelist.net/{genre['type']}/genre/{genre['mal_id']})")
                    else:
                        arrgenres.append(genre['name'])
                embed.add_field(name=name, value=', '.join(
                    arrGenres), inline=False)
        if await checkExists('episodes', data):
            embed.add_field(name='Episodes',
                            value=f"`{data['episodes']}`", inline=True)
        elif await checkExists('chapters', data):
            embed.add_field(name='Chapters',
                            value=f"`{data['chapters']}`", inline=True)
        if await checkExists('status', data):
            if type == 'anime':
                if await checkExists('airing', data):
                    if data['airing'] == 'true':
                        air = 'Airing'
                    elif data['airing'] == 'false':
                        air = 'Aired'
                if await checkExists('aired', data):
                    if await checkExists('from', data['aired']):
                        if await checkExists('to', data['aired']):
                            embed.add_field(
                                name='Airing Status', value=f"{air} `{data['aired']['from'].split('T')[0]}` to `{data['aired']['to'].split('T')[0]}`", inline=True)
                        else:
                            embed.add_field(
                                name='Airing Status', value=f"{air} `{data['aired']['from'].split('T')[0]}`", inline=True)
                    else:
                        embed.add_field(name='Airing Status',
                                        value=air, inline=True)
                else:
                    embed.add_field(name='Airing Status',
                                    value=data['status'], inline=True)
            elif type == 'manga':
                if await checkExists('publishing', data):
                    if data['publishing'] == 'true':
                        air = 'Publishing'
                    elif data['publishing'] == 'false':
                        air = 'Published'
                if await checkExists('published', data):
                    if await checkExists('from', data['published']):
                        if await checkExists('to', data['published']):
                            embed.add_field(
                                name='Publishing Status', value=f"{air} `{data['published']['from'].split('T')[0]}` to `{data['published']['to'].split('T')[0]}`", inline=True)
                        else:
                            embed.add_field(
                                name='Publishing Status', value=f"{air} `{data['published']['from'].split('T')[0]}`", inline=True)
                    else:
                        embed.add_field(name='Publishing Status',
                                        value=air, inline=True)
                else:
                    embed.add_field(name='Publishing Status',
                                    value=data['status'], inline=True)
        if await checkExists('source', data):
            embed.add_field(
                name='Origin', value=f"`{data['source']}`", inline=True)
        if await checkExists('licensors', data):
            if len(data['licensors']) > 0:
                name = 'Licensor'
                arrLicensors = []
                if len(data['licensors']) > 1:
                    name = 'Licensors'
                for licensor in data['licensors']:
                    if await checkExists('url', licensor):
                        arrLicensors.append(
                            f"[{licensor['name']}](https://myanimelist.net/anime/producer/{licensor['mal_id']})")
                    else:
                        arrLicensors.append(licensor['name'])
                embed.add_field(name=name, value=', '.join(arrLicensors))
        if await checkExists('studios', data):
            if len(data['studios']) > 0:
                name = 'Studio'
                arrstudios = []
                if len(data['studios']) > 1:
                    name = 'Studios'
                for studio in data['studios']:
                    if await checkExists('url', studio):
                        arrstudios.append(
                            f"[{studio['name']}](https://myanimelist.net/anime/producer/{studio['mal_id']})")
                    else:
                        arrstudios.append(studio['name'])
                embed.add_field(name=name, value=', '.join(arrstudios))
        if await checkExists('authors', data):
            if len(data['authors']) > 0:
                name = 'author'
                arrauthors = []
                if len(data['authors']) > 1:
                    name = 'authors'
                for author in data['authors']:
                    if await checkExists('url', author):
                        arrauthors.append(
                            f"[{author['name']}](https://myanimelist.net/people/{author['mal_id']})")
                    else:
                        arrauthors.append(author['name'])
                embed.add_field(name=name, value=', '.join(arrauthors))
        return embed
    else:
        raise JikanError()
        return None


async def search(session, query, type, limit=4):
    #query = requests.utils.quote(query,safe='')
    data = await RLRequest(session, f'{baseAPIURL}/search/{type}?q={query}&page=1&limit={limit}')
    result = []
    if data:
        if await checkExists('results', data):
            if len(data['results']) > 0:
                for searchResult in data["results"]:
                    result.append([searchResult['title'], searchResult['type'],
                                   searchResult['image_url'], searchResult['mal_id']])
                return result
            else:
                raise JikanError(
                    f'Sorry, I couldn\'t find any results for \'{query}\'')
                return None
        else:
            raise JikanError(
                f'Sorry, I couldn\'t find any results for \'{query}\'')
            return None
    else:
        raise JikanError()
        return None


class MyAnimeList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mal(self, ctx, *args):
        if args[0].lower() == 'id':
            data = await fetchItem(session, ''.join(args[1:]).upper())
            if data:
                embed = await formatItem(session, data)
                await ctx.send(embed=embed)
        elif args[0].lower() == 'qa':  # Quick Anime (searches and displays the first result)
            query = str(''.join(args[1:])).lower()
            data = await search(session, query, 'anime', 1)
            if data:
                data = await fetchItem(session, f'A/{data[0][3]}')
                if data:
                    embed = await formatItem(session, data)
                    if embed:
                        await ctx.send(embed=embed)
        elif args[0].lower() == 'qm':  # Quick Manga (searches and displays the first result)
            query = str(''.join(args[1:])).lower()
            data = await search(session, query, 'manga', 1)
            if data:
                data = await fetchItem(session, f'M/{data[0][3]}')
                if data:
                    embed = await formatItem(session, data)
                    if embed:
                        await ctx.send(embed=embed)
        else:  # search
            query = str(''.join(args[0:])).lower()
            if query.startswith('m/') or query.startswith('m '):
                searchType = 'M'
                data = await search(session, query, 'manga')
            else:
                searchType = 'A'
                data = await search(session, query, 'anime')
            if data:
                reference = {'user': str(ctx.author.id)}
                desc = ''
                for i in range(0, len(data)):
                    result = data[i]
                    desc = f'{desc}{regionalindicators[i]} [{result[1]}][{result[0]}]\n'
                    reference[regionalindicators[i]
                              ] = f'{searchType}/{result[3]}'
                embed = discord.Embed(
                    color=0x2e51a2, title=f'Search for \'{query}\'', description=desc)
                msg = await ctx.send(embed=embed)
                menus[f'{ctx.guild.id}|{msg.id}'] = reference
                for i in range(0, len(data)):
                    await msg.add_reaction(regionalindicators[i])
                await msg.delete(delay=30)
                await ctx.message.delete()
            else:
                raise JikanError()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        idMessage = payload.message_id
        idGuild = payload.guild_id
        idChannel = payload.channel_id
        idUser = payload.user_id
        emoji = payload.emoji.name
        index = f'{idGuild}|{idMessage}'
        if str(idUser) == str(menus[index]['user']):
            if emoji in menus[index]:
                embed = discord.Embed(color=0x2e51a2)
                channel = self.bot.get_channel(idChannel)
                data = await fetchItem(session, str(menus.pop(index)[emoji]))
                if data:
                    embed = await formatItem(session, data)
                # else:
                    # embed = await generateErrorEmbed('Sorry, there was an unexpected error!')
                    await channel.send(embed=embed)
                message = await channel.fetch_message(idMessage)
                await message.delete()


class JikanError(APIError):
    # raised when jikan returns an error (!200)
    def __init__(self, message='Jikan API Error.'):
        super().__init__(message)


class InvalidID(commands.BadArgument):
    # raised when the specified ID doesn't exist
    def __init__(self, message='Invalid ID.'):
        super().__init__(message)


def setup(bot):
    bot.add_cog(MyAnimeList(bot))
