const Discord = require("discord.js");
const config = require("./config.json")

var bot = new Discord.Client();

bot.on("ready", () =>{
	console.log("Rensouhou Board Module ver 1.0 is now active");
});

bot.on("messageReactionAdd", (reaction, user) =>{
  if (reaction.message.guild.channels.exists("name", "board") != false) {
    if (reaction.emoji.name !== '⭐') return;
    const boardID = reaction.message.guild.channels.find("name","board")
    if (reaction.message.channel.name === "board") return;
    if (reaction.count === 3) {
      const boardMSG = new Discord.RichEmbed()
      .setAuthor(reaction.message.author.username, reaction.message.author.avatarURL)
      .setDescription (reaction.message.content)
      .setTimestamp(new Date())
      .setColor(0x00AE86)
      reaction.message.guild.channels.find("name","board").send(boardMSG)
    }
  } else {
    reaction.message.channel.send("I'm sorry but you don't have a #board channel yet!")
  }
});

bot.login(config.token);