"""
Administration commands.
Mostly requires elevated permissions.
Carlos Saucedo, 2020
"""

import discord
from discord.ext import commands
import sqlite3
from Cogs.Errors import APIError


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def prefix(self, ctx, arg):
        """
        Sets the prefix to the provided argument.
        """
        conn = sqlite3.connect("db/database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM PREFIXES WHERE server=?;",
                  [ctx.channel.guild.id])
        if(len(c.fetchall()) == 0):
            # The prefix has not seriously been set
            c.execute("INSERT INTO prefixes VALUES (?,?);",
                      str(ctx.channel.guild.id), arg)
            await ctx.send("Set prefix to `"+arg+"`!")
        else:
            c.execute(
                '''
                UPDATE prefixes
                SET prefix=?
                WHERE server=?;
                ''',
                [arg, str(ctx.channel.guild.id)]
            )
            await ctx.send("Set prefix to `"+arg+"`!")
        conn.commit()
        conn.close()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, arg):
        """
        Bans the specified user.
        """
        try:
            user = ctx.message.mentions[0]
            await ctx.message.guild.ban(user)
            await ctx.send("Banned `"+user.name+"`.")
        except Exception as e:
            raise APIError(str(e))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, arg):
        """
        Kicks the specified user.
        """
        try:
            user = ctx.message.mentions[0]
            await ctx.message.guild.kick(user)
            await ctx.send("Kicked `"+user.name+"`.")
        except Exception as e:
            raise APIError(str(e))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, arg):
        """
        Clears a set number of messages from the channel.
        """
        if(len(ctx.message.mentions) != 0):
            # Clear a user's messages.
            messages = []
            async for msg in ctx.message.channel.history():
                if(msg.author == ctx.message.mentions[0]):
                    messages.append(msg)
            if(len(messages) < 1):
                await ctx.send("Could not find any messages from the specified user.")
            else:
                await ctx.message.channel.delete_messages(messages)
                await ctx.send("Deleted `"+str(len(messages))+"` messages!")
        else:
            await ctx.message.channel.purge(limit=(int(arg)+1), bulk=True)
            await ctx.send("Deleted "+str(arg)+" messages!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def mute(self, ctx, arg):
        """
        Mutes the specified user.
        """
        if(len(ctx.message.mentions) > 0):
            sinner = ctx.message.mentions[0]
            await ctx.message.channel.set_permissions(sinner, send_messages=False)
            await ctx.send("Muted {0.mentions[0].mention}1".format(ctx.message))
        else:
            await ctx.send("You must specify a user.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def unmute(self, ctx, arg):
        """
        Unmutes the specified user.
        """
        if(len(ctx.message.mentions) > 0):
            await ctx.message.channel.set_permissions(ctx.message.mentions[0], send_messages=True)
            await ctx.send("Unmuted {0.mentions[0].mention}!".format(ctx.message))
        else:
            await ctx.send(ctx.message.channel.send("You must specify a user."))


def setup(bot):
    bot.add_cog(Admin(bot))
