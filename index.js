const dotenv = require("dotenv");
const fs = require('fs');
const { Client, Collection, Intents } = require('discord.js');

dotenv.config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS] });

client.commands = new Collection();
const commandFiles = fs.readdirSync("./commands").filter(file => file.endsWith(".js"));

for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.data.name, command);
}

client.on("interactionCreate", async interaction => {

    const command = client.commands.get(interaction.commandName);

    if (!command) return;

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        interaction.reply({ content: "There was an error while executing this command", ephemeral: true })
        .catch(console.error);
    }
});

client.once("ready", () => {
    console.log("CultBot Ready");
});

client.login(process.env.DISCORD_TOKEN);