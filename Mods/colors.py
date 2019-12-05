"""
Color roles module for Rikka.
Carlos Saucedo, 2019
"""
import sqlite3
import json
import discord


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


def getColor(name):
    """
    Generates a discord.Color object from the color name as a string.
    """
    with open("json/css-color-names.json", "r") as h:
        colors = json.load(h)
    colorHex = colors.get(name)
    if(colorHex is None):
        return None
    else:
        colorHex = colorHex.lstrip('#')
        return discord.Color(int(colorHex, 16))
