# rikka-bot [![Support me on Patreon!](https://cdn.discordapp.com/attachments/437991897269665792/446474035149144074/unknown.png)](https://www.patreon.com/LeoSaucedo)

A Discord bot that performs various functions.

![Python 3.6](https://img.shields.io/badge/python-3.5%2C%203.6-blue.svg) [![Discord Bots](https://discordbots.org/api/widget/status/430482288053059584.svg)](https://discordbots.org/bot/430482288053059584) [![Discord Bots](https://discordbots.org/api/widget/servers/430482288053059584.svg)](https://discordbots.org/bot/430482288053059584)

## Table of Contents

1. [Commands](#commands)
   - [Main Commands](#main-commands)
     - [Utility Commands](#utility-commands)
     - [Admin Commands](#admin-commands)
   - [Self-Assignable Roles](#self-assignable-roles)
     - [Enabling/Disabling/Listing](#enablingdisablinglisting)
     - [Assigning/Unassigning Roles](#assigningunassigning-roles)
   - [Color Role System](#color-role-system)
     - [Setup](#setup)
     - [Usage](#usage)
   - [Economy System](#economy-system)
   - [Fun Commands](#fun-commans)
     - [XKCD Commands](#xkcd-commands)
     - [GIF Commands](#gif-commands)
     - [Gelbooru Commands](#gelbooru-commands)
     - [Emotes](#emotes)
   - [Game Commands](#game-commands)
     - [Trivia Commands](#trivia-commands)
     - [Casino Commands](#casino-commands)
2. [In The Works](#in-the-works)
3. [Special Thanks](#special-thanks)

## Commands

_Right now, this bot's prefix is_ `;`_._

### Main Commands

#### Utility Commands

- `@mention help` - Returns a command list, along with your server's prefix.
- `;help` - Returns a command list.
- `;info` - Returns information about the bot.
- `;paypal` - Returns donation link to contribute to server hosting.
- `;vote` - Returns this server's vote link on [discordbots.org](https://discordbots.org/).
- `;clever (text)` - Returns the cleverbot response to the given text.        
- `;gizoogle (text)` - Translates a given text with gizoogle.
- `;translate (text)` - Translates the specified text to English.
- `;suggest (suggestion)` - Adds a completely anonymous suggestion to better the bot.
- `;quickvote (vote)` - Creates a message with thumbs up and thumbs down, in a pretty text embed.
- `;sayd (message)` - Allows you to say an anonymous message by saying what you tell it to, and then deleting your message. Prevents `@everyone`, of course.
- `;wolfram (query)` - Queries a response to Wolfram Alpha.

#### Admin Commands

- `;prefix (prefix)` - Changes the prefix to a set custom prefix. _(Must be admin)_
- `;clear (number)` - Clears a set number of messages from the given channel. _(Must have manage message permission)_
- `;clear (user)` - Clears any messages authored by the specified user in the channel. _(Must have manage message permission)_
- `;mute / ;unmute (user)` - Mutes/unmutes specified user. _(Must have manage message permission)_
- `;kick (user)` - Kicks the specified user. _(Must have kick permission)_
- `;ban (user)` - Bans the specified user. _(Must have ban permission)_
- `;add (points) (user(s))` - Adds a set number of points to mentioned user(s). _(Must be admin)_
- `;subtract (points) (user(s))` - Subtracts a set number of points from mentioned user(s). _(Must be admin)_

### Self-Assignable Roles

_NOTE: In order to do this, Rikka must be placed above the users you would like to enable assigning to. Failure to do so will fail to assign the roles._

Rikka has a self-assignable roles system. If it is enabled for your server, you can create roles to assign yourself and other users.
For these commands to work, the role names must match perfectly.

#### Enabling/Disabling/Listing

- `;iamlist` - Lists the assignable roles.
- `;assign enable (role name)` - Enables assignability for the given role. _(Must have Manage Roles permission)_
- `;assign disable (role name)`- Disables assignability for the given role. _(Must have Manage Roles permission)_

#### Assigning/Unassigning Roles

- `;iam (role name)` - Assigns yourself the role.
- `;iamnot (role name)` - Unassigns yourself the role.

### Color Role System

_NOTE: In order to do this, Rikka must be placed above the roles whose colors you would like to override. Failure to do so will just create and assign the role without any effect._

Rikka has a color role system. If it is enabled for your server, you can set your own color from the image below.

![Color Chart](https://raw.githubusercontent.com/LeoSaucedo/rikka-bot/master/json/css-color-names.png)

#### Setup

_Setup requires manage roles permission._

- `;colors (enable/disable)` - enables or disables the color role mode for your server.

#### Usage

- `;color (color)` - Sets your color to the specified color.
- `;color reset` - Removes all of your color roles, resetting you to your original color.

### Economy System

Rikka's economy system consists of a global leaderboard. Currently, you can get points in two ways: Getting questions right with the `;trivia` command, and collecting points daily.

- `;score` - Displays your score, or another user's score, globally.
- `;collect daily` - Gets your daily collections.
- `;leaderboard global` - View the global leaderboard across all of rikka's servers.
- `;leaderboard local` - View the local leaderboard across all of the users on the current server.
- `;give (points) (user)` - donate points to another user.

### Fun Commands

- `;insult (user)` - Sends a random insult to the given user.
- `;ramsay` - Returns a random Gordon Ramsay quote.
- `;gay` - no u
- `;rate (thing to rate)` - Rates whatever you tell it to rate on a scale of 1-10.
- `;ping` - For that annoying person who keeps `@everyone`ing.
- `;beemovie` - Returns a random bee movie quote.

#### MAL Commands

- `;mal (anime)` - Returns the result of the anime search.
- `;mal m/(manga)` - Returns the result of the manga search.
- `;malqa (anime)` - Returns the result of the anime search.
- `;malqm (manga)` - Returns the result of the manga search.
- `;mal id a/(anime id)` - Returns the result of the anime ID search.
- `;mal id m/(manga id)` - Returns the result of the manga ID search.

#### XKCD Commands

- `;xkcd` - Returns a random XKCD comic.
- `;xkcd (number)` - Returns a specific XKCD comic.
- `;xkcd latest` - Returns the latest XKCD comic.

#### Gif Commands

- `;hello` - Says hi.
- `;hugme` - Hugs you.
- `;hug @user` - Hugs the specified user.

#### Emotes

_Note: All emotes are entirely SFW._

- `shocked, smile, hentai, blush, bdsm, rekt, boop, fuckoff, sanic, dreamy, kys`

#### Gelbooru Commands

_These commands require the channel to be marked as NSFW._

- `;gelbooru random` - Fetches a random gelbooru post.
- `;gelbooru latest` - Fetches the latest gelbooru post.
- `;gelbooru tags (tags, comma separated)` - Fetches a post that matches the specified tags.

### Game Commands

#### Trivia Commands

- `;trivia` - Returns the help menu for trivia.
- `;ask` - Returns a randomly selected question.
- `;a (attempt)` - Tests the given attempt to see if it is correct. If it is correct, you are granted a point.
- `;reveal` - Reveals the answer, removing the ability to score for that specific question.

#### Casino Commands

- `;roll` - Rolls a die.
- `;flip` - Flips a coin.
- `;8ball (question)` - Tells you the future.
- `;raffle` - Select a random (non-bot) user from your server

### Board Functionality

_This feature is currently not functional. Sorry!_

The board functionality allows popular messages to be posted on a special channel, titled `board`.
To use this functionality, you must first run `;board enable`.
Afterwards, every message with 3 reactions with the "⭐" will get posted to the board.

#### In the works

- Improved, proprietary AI, instead of cleverbot.
- Aliases for Self-Assignable Roles
- Minecraft Server Status

### Special Thanks

- Special thanks to user chafla for their code [gizoogle.py](https://github.com/chafla/gizoogle-py), which helped make this program possible.
- Hat tip to Rapptz for developing the [Discord API Wrapper](https://github.com/Rapptz/discord.py) used in this program.
- Credit to phl4nk for their [implementation of the cleverbot.io API for python](https://github.com/phl4nk/CleverApi).
- Thanks to [Wes](https://github.com/NeonWizard) for his [website](http://wizardlywonders.xyz:3054/) that generates the Bee Movie quotes!
- Of course, credit to [XKCD](https://xkcd.com/) for the wonderful comic that is a great feature of this bot.
- Kudos to [bahamas10](https://github.com/bahamas10) for his [list](https://github.com/bahamas10/css-color-names/blob/master/css-color-names.json) of CSS color names!
