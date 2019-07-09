"""
Self-assignable assign_roles module for Rikka.
Carlos Saucedo, 2019
"""
import sqlite3

def setAssign(serverId, roleId, status):
    """Sets the assignability of a certain role."""

    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()


    if(status):
        # Enable the role.
        c.execute('''
        SELECT role FROM assign_roles WHERE role=?
        ''', (str(roleId),))
        if(c.fetchone() == None):
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
    if(c.fetchone() == None):
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