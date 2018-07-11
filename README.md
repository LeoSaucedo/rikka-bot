![Python 3.5, 3.6](https://img.shields.io/badge/python-3.5%2C%203.6-blue.svg) [![Discord Bots](https://discordbots.org/api/widget/status/430482288053059584.svg)](https://discordbots.org/bot/430482288053059584) [![Discord Bots](https://discordbots.org/api/widget/servers/430482288053059584.svg)](https://discordbots.org/bot/430482288053059584)


[![Support me on Patreon!](https://cdn.discordapp.com/attachments/437991897269665792/446474035149144074/unknown.png)](https://www.patreon.com/LeoSaucedo)
# rikka-bot

A Discord bot that performs various functions.

### Commands
*Right now, this bot's prefix is* `;`*.*

##### Economy System
Rikka's economy system consists of a global leaderboard. Currently, you can get points in two ways: Getting questions right with the `;trivia` command, and upvoting the bot.
- `;score` - Displays your score, or another user's score, globally.
- `;collect daily` - Gets your daily collections.
- `;leaderboard global` - View the global leaderboard across all of rikka's servers.
- `;leaderboard local` - View the local leaderboard across all of the users on the current server.
- `;givepoints (points) (user)` - donate points to another user.

##### Board Functionality
The board functionality allows popular messages to be posted on a special channel, titled `board`.
To use this functionality, you must first run `;board enable`.
Afterwards, every message with 3 reactions with the "⭐" will get posted to the board.

##### Utility Commands
- `;help` - Returns a command list.
- `;info` - Returns information about the bot.
- `@mention help` - Returns a command list.
- `;paypal` - Returns donation link to contribute to server hosting.
- `;vote` - Returns this server's vote link on [discordbots.org](https://discordbots.org/).
- `;clever (text)` - Returns the cleverbot response to the given text.
- `;gizoogle (text)` - Translates a given text with gizoogle.
- `;translate (text)` - Translates the specified text to English.
- `;suggest (suggestion)` - Adds a completely anonymous suggestion to better the bot.
- `;quickvote (vote)` - Creates a message with thumbs up and thumbs down, in a pretty text embed.

##### Fun Commands
- `;insult (user)` - Sends a random insult to the given user.
- `;ramsay` - Returns a random Gordon Ramsay quote.
- `;gay` - no u
- `;rate (thing to rate)` - Rates whatever you tell it to rate on a scale of 1-10.
- `;ping` - For that annoying person who keeps `@everyone`ing.
- `;beemovie` - Returns a random bee movie quote.
- `;xkcd` - Returns a random XKCD comic.
- `;xkcd (number)` - Returns a specific XKCD comic.
- `;xkcd latest` - Returns the latest XKCD comic.

##### Gif Commands
- `;hello` - Says hi.
- `;hugme` - Hugs you.
- `;hug @user` - Hugs the specified user.

##### Trivia Commands
- `;trivia` - Returns the help menu for trivia.
- `;ask` - Returns a randomly selected question.
- `;a (attempt)` - Tests the given attempt to see if it is correct. If it is correct, you are granted a point.
- `;reveal` - Reveals the answer, removing the ability to score for that specific question.

##### Casino Commands
- `;roll` - Rolls a die.
- `;flip` - Flips a coin.
- `;8ball (question)` - Tells you the future.
- `;raffle` - Select a random (non-bot) user from your server

##### Admin Commands
- `;prefix (prefix)` - Changes the prefix to a set custom prefix. *(Must be admin)*
- `;clear (number)` - Clears a set number of messages from the given channel. *(Must have manage message permission)*
- `;clear (user)` - Clears any messages authored by the specified user in the channel. *(Must have manage message permission)*
- `;mute / ;unmute (user)` - Mutes/unmutes specified user. *(Must have manage message permission)*
- `;kick (user)` - Kicks the specified user. *(Must have kick permission)*
- `;ban (user)` - Bans the specified user. *(Must have ban permission)*
- `;addpoints (points) (user(s))` - Adds a set number of points to mentioned user(s). *(Must be admin)*
- `;subtractpoints (points) (user(s))` - Subtracts a set number of points from mentioned user(s). *(Must be admin)*

##### Emotes
*Note: All emotes are entirely SFW.*
- `shocked, smile, hentai, blush, bdsm, rekt, boop, fuckoff, sanic, dreamy, kys`

#### In the works
- Dynamic "playing" statuses for communication between devs and member servers.
- Improved, proprietary AI, instead of cleverbot.
- Marry RP function

### Special Thanks
- Special thanks to user chafla for their code [gizoogle.py](https://github.com/chafla/gizoogle-py), which helped make this program possible.
- Hat tip to Rapptz for developing the [Discord API Wrapper](https://github.com/Rapptz/discord.py) used in this program.
- Credit to phl4nk for their [implementation of the cleverbot.io API for python](https://github.com/phl4nk/CleverApi).
- Thanks to [Wes](https://github.com/NeonWizard) for his [website](http://wizardlywonders.xyz:3054/) that generates the Bee Movie quotes!
- Of course, credit to [XKCD](https://xkcd.com/) for the wonderful comic that is a great feature of this bot.
