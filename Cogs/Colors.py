"""
Colors module.
Carlos Saucedo, 2020
"""
import discord
import json
from discord.ext import commands
import sqlite3


class Colors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def colors(self, ctx, status):
        """
        Enables or disables colors in the guild.
        """
        if(status == "enable"):
            # Enable colors.
            setColorMode(True, ctx.guild.id)
            await ctx.send("Enabled custom user colors!")

        elif(status == "disable"):
            # Disable colors.
            setColorMode(False, ctx.guild.id)
            await ctx.send("Disabled custom user colors.")
        else:
            # Invalid arg
            raise commands.BadArgument(
                "Invalid option. only enable/disable permitted.")

    @commands.hybrid_command()
    async def color(self, ctx, color):
        """
        Set your color role.
        """
        if(getColorMode(ctx.guild.id)):
            # Colors are enabled
            colorObj = getColor(color)
            if(colorObj == None):
                raise commands.BadArgument("Invalid color name.")
            else:
                # Returns a color object.
                roleCreated = False
                # Removing any previously added roles.
                for role in ctx.author.roles:
                    if(role.name.startswith("Color - ")):
                        await ctx.author.remove_roles(role)
                # Searching to see if role is in server.
                for role in ctx.guild.roles:
                    if(role.name == ("Color - " + color)):
                        roleCreated = True
                        # Place the role directly under the bots top role position.
                        await role.edit(position=(ctx.guild.me.top_role.position-1))
                        await ctx.author.add_roles(role)
                        break
                if(not roleCreated):
                    # If the role has not been created.
                    # Remove the previously existing role if applicable
                    # Create a new role with the specified color.
                    newRole = await ctx.guild.create_role(color=colorObj, name=("Color - "+color))
                    # Place role directly under bot's top role pos.
                    await newRole.edit(position=(ctx.me.top_role.position-1))
                    await ctx.author.add_roles(newRole)
                await ctx.send(("{0.author.mention}, changed your color to " +
                                color + "!").format(ctx.message))
        else:
            raise commands.BadArgument(
                "Color roles are not enabled for this server.")
    
    #used in inv cmd to change the color role
    async def inv_color(self, ctx, userName, hex):
        """Sets color role from users inventory"""
        colorObj = getColor(userName, hex)
        roleCreated = False
        # Removing any previously added roles.
        for role in ctx.author.roles:
            if(role.name.startswith("Color - ")):
                await ctx.author.remove_roles(role)
        # Searching to see if role is in server.
        for role in ctx.guild.roles:
            if(role.name == ("Color - " + userName)):
                roleCreated = True
                # Place the role directly under the bots top role position.
                await role.edit(position=(ctx.guild.me.top_role.position-1), color = colorObj)
                await ctx.author.add_roles(role)
                break
        if(not roleCreated):
            # If the role has not been created.
            # Remove the previously existing role if applicable
            # Create a new role with the specified color.
            newRole = await ctx.guild.create_role(color=colorObj, name=("Color - "+userName))
            # Place role directly under bot's top role pos.
            await newRole.edit(position=(ctx.me.top_role.position-1))
            await ctx.author.add_roles(newRole)
        await ctx.send(("{0.author.mention}, changed your color to " +
                            hex + "!").format(ctx.message))

async def setup(bot):
    await bot.add_cog(Colors(bot))


def setColorMode(status, serverID):
    """
    Set the color mode to the specified state.
    """
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()

    if(status):
        status = "1"
    else:
        status = "0"

    c.execute("SELECT color_roles FROM server_settings WHERE server=?",
              (str(serverID),))
    if(c.fetchone() is None):
        # If there is no entry.
        c.execute('''
        INSERT INTO server_settings (server, color_roles)
        VALUES (?, ?);
        ''', (str(serverID), str(status)))
    else:
        # There is already an entry in the db
        c.execute('''
        UPDATE server_settings
        SET color_roles=?
        WHERE server=?
        ''', (str(status), str(serverID)))
    conn.commit()
    conn.close()


def getColorMode(serverID):
    """
    Returns whether the color mode is enabled.
    """
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()
    c.execute("SELECT color_roles FROM server_settings WHERE server=?",
              (str(serverID),))
    if(c.fetchone() is None):
        return False
    else:
        c.execute(
            "SELECT color_roles FROM server_settings WHERE server=?", (str(serverID),))
        if(c.fetchone()[0] == 1):
            return True
        return False


def getColor(name, hex=None):
    """
    Generates a discord.Color object from the color name as a string.
    """
    if hex == None:
        with open("json/css-color-names.json", "r") as h:
            colors = json.load(h)
        colorHex = colors.get(name)
        if(colorHex is None):
            return None
        else:
            colorHex = colorHex.lstrip('#')
            return discord.Color(int(colorHex, 16))
    else:
        hex = hex.lstrip('#')
        return discord.Color(int(hex, 16))
