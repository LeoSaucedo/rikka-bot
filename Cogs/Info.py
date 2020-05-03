import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """Sends the user information about the bot.

        Args:
            ctx (discord.ext.commands.Context): The message context.
        """
        msg = "Hi there! I'm Rikka. This bot was created by Leo. This server's command prefix is: `" + \
            ctx.prefix + "`. To get help use `"+ctx.prefix+"help`."
        await ctx.send(msg)

    @commands.command()
    async def hello(self, ctx):
        """Says hello to the user.

        Args:
            ctx (discord.ext.commands.Context): The message context.
        """
        msg = "h-hello {0.author.mention}-chan!".format(ctx.message)
        + "https://cdn.discordapp.com/attachments/402744318013603840/430592483282386974/image.gif"
        await ctx.send(msg)

    @commands.command()
    async def codeformat(self, ctx):
        """Explains how to format code in Discord.

        Args:
            ctx (discord.ext.commands.Context): The message context.
        """
        msg = ("To use discord's muliline code formatting, send your message with the following template:\n"
               + "\`\`\`python\nprint(\"Hello, World\")\n\`\`\`\n\n"
               + "This outputs:\n```python\nprint(\"Hello, World\")\n```\n"
               + "Replace \"python\" with the language you are using to get some pretty syntax highlighting!")
        await ctx.send(msg)

    @commands.command()
    async def donate(self, ctx):
        """Returns the Patreon donation link.

        Args:
            ctx (discord.ext.commands.Context): The message context.
        """
        await ctx.send("Help my programmer out, become a patron today! https::www.patreon.com/LeoSaucedo")

    @commands.command()
    async def vote(self, ctx):
        """Returns the dbl vote link.

        Args:
            ctx (discord.ext.commands.Context): The message context.
        """
        await ctx.send("Vote for me to take over the world! https://discordbots.org/bot/430482288053059584/vote")

    @commands.command()
    async def latency(self, ctx):
        """Returns the latency of the bot.

        Args:
            ctx (discord.ext.commands.Context): The message context.
        """
        await ctx.send("Latency: " + str(int(ctx.bot.latency * 1000)) + "ms")


def setup(bot):
    bot.add_cog(Info(bot))
