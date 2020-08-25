"""
Roles module.
Carlos Saucedo, 2020
"""
import discord
from discord.ext import commands
import sqlite3
from Cogs.Errors import APIError


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def assign(self, ctx, status, roleName):
        """"
        Enables or disables the given role for assignment.
        """
        role = discord.utils.get(ctx.guild.roles, name=(roleName))
        if(status == "enable"):
            # Enable assignment
            if(role == None):
                # Role does not exist, create new role
                role = await ctx.guild.create_role(name=str(roleName))
            # Role already exists
            # Set the role as assignable
            setAssign(ctx.guild.id, role.id, True)
            await ctx.send("Enabled role `{}` assignment!"
                           .format(role.name))
        elif(status == "disable"):
            # Disable assignment
            if(role == None):
                raise commands.BadArgument("Role does not exist.")
                return
            else:
                setAssign(ctx.guild.id, role.id, False)
                await ctx.send("Disabled role `{}` assignment."
                               .format(role.name))
        else:
            # Invalid arg
            raise commands.BadArgument(
                "Invalid option. Only enable/disable permitted.")
            return

    @commands.command()
    async def iamlist(self, ctx):
        """
        Lists the assignable roles.
        """
        assignList = ""
        assignableRoles = getAssignList(ctx.guild.id)
        if(len(assignableRoles) > 0):
            for role in assignableRoles:
                # If the role still exists, add it to the list of assignable roles.
                roleObject = discord.utils.get(
                    ctx.guild.roles, id=int(role[0]))
                if roleObject != None:
                    # If the role still exists in the server,
                    # Add it to the print list.
                    roleName = roleObject.name
                    assignList += roleName+"\n"
                else:
                    # If the role doesn't exist anymore, delete it from the database.
                    assign.setAssign(ctx.guild.id, int(role[0], False))
            if(assignList != ""):
                assignEmbed = discord.Embed(
                    title="Assignable Roles",
                    color=0x4287f5,
                    description=assignList
                )
                await ctx.channel.send(embed=assignEmbed)
        else:
            await ctx.send("{0.author.mention}, no assignable roles have been set."
                           .format(ctx.message))

    @commands.command()
    async def iam(self, ctx, roleName):
        """
        Assigns you to the specified role.
        """
        # Check to see if role exists.
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if(role == None):
            # Role does not exist
            await ctx.send("{0.author.mention}, that role does not exist!"
                           .format(ctx.message))
        else:
            # Role exists
            if(isAssignable(role.id)):
                # If role is assignable.
                if(discord.utils.get(ctx.author.roles, id=role.id) == None):
                    # Role is not already assigned
                    await ctx.author.add_roles(role)
                    await ctx.send("{0.author.mention}, role `".format(ctx.message)
                                   + role.name + "` has been assigned.")
                else:
                    # Role is already assigned
                    await ctx.send("{0.author.mention}, that role is already assigned to you!".format(
                        ctx.message))

    @commands.command()
    async def iamnot(self, ctx, roleName):
        """
        Unassigns you from the specified role.
        """
        # Check to see if role exists.
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if(role == None):
            # Role does not exist
            await ctx.send("{0.author.mention}, that role does not exist!"
                           .format(ctx.message))
        else:
            # Role exists
            if(isAssignable(role.id)):
                if(discord.utils.get(ctx.author.roles, id=role.id) == None):
                    await ctx.send("{0.author.mention}, that role is not assigned to you!".format(ctx.message))
                else:
                    await ctx.author.remove_roles(role)
                    await ctx.send("{0.author.mention}, role `".format(ctx.message)
                                   + role.name + "` has been unassigned.")


def setAssign(serverId, roleId, status):
    """Sets the assignability of a certain role."""

    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()

    if(status):
                # Enable the role.
        c.execute('''
        SELECT role FROM assign_roles WHERE role=?
        ''', (str(roleId),))
        if(c.fetchone() is None):
                    # If there is no entry,
                    # Add the entry to the database.
            c.execute('''
            INSERT INTO assign_roles (server, role)
            VALUES (?,?);
            ''', (str(serverId), str(roleId)))
    else:
        # Disable the role.
        # Delete the entry from the database.
        c.execute('''
        DELETE FROM assign_roles WHERE role=?
        ''', (str(roleId),))

    conn.commit()
    conn.close()


def isAssignable(roleId):
    """Verifies whether the role is assignable."""
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()

    c.execute('''
    SELECT role FROM assign_roles WHERE role=?
    ''', (str(roleId),))
    if(c.fetchone() is None):
        # If the role isn't in the database, aka
        # If the role isn't enabled.
        return(False)
    else:
        return(True)

    conn.commit()
    conn.close()


def getAssignList(serverId):
    """Fetches the assignable roles for the given server."""
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()

    c.execute("SELECT role FROM assign_roles WHERE server=?", (str(serverId),))
    assignList = c.fetchall()
    c.close()

    return assignList


def setup(bot):
    bot.add_cog(Roles(bot))
