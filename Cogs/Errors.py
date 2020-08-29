"""
Error Handling Module.
Carlos Saucedo, 2020
"""

import discord
import traceback
import sys
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # Defining error types
        internal = (commands.CommandNotFound)
        pebkac = (commands.BadArgument,
                  commands.BotMissingPermissions,
                  commands.MissingPermissions,
                  commands.ExtensionAlreadyLoaded,
                  commands.ExtensionNotLoaded,
                  commands.ExtensionNotFound,
                  commands.MissingRequiredArgument,
                  APIError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, internal):
            return
        elif isinstance(error, pebkac):
            return await ctx.send(embed=(await generateErrorEmbed(str(error))))

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(
            ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr)


class APIError(commands.CommandError):
    """Represents an error in the API.
    """

    def __init__(self, message="API Error."):
        super().__init__(message)


async def generateErrorEmbed(msg):
    return discord.Embed(color=0xff0000, title="Error", description=msg)


def setup(bot):
    bot.add_cog(Errors(bot))
