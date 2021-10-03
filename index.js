const dotenv = require("dotenv");
const fs = require('fs');
const { Sequelize, DataTypes } = require('sequelize');
const { Client, Collection, Intents } = require('discord.js');

const { positive, negative } = require("./emojiConfig.json");

dotenv.config();

const sequelize = new Sequelize({
    dialect: "sqlite",
    storage: "./database.sqlite"
});

const User = sequelize.define("User", {
    userId: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
    },
    karma: {
        type: DataTypes.INTEGER,
        allowNull: false,
        defaultValue: 0
    },
    blacklisted: {
        type: DataTypes.BOOLEAN,
        allowNull: false,
        defaultValue: false
    },
    colour: {
        type: DataTypes.STRING,
        allowNull: false,
        defaultValue: "8b01e6"
    }
});

const client = new Client({ 
    intents: [
        Intents.FLAGS.GUILDS, 
        Intents.FLAGS.GUILD_MESSAGE_REACTIONS, 
        Intents.FLAGS.GUILD_EMOJIS_AND_STICKERS
    ] 
});

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
        await command.execute(interaction, User);
    } catch (error) {
        console.error(error);
        interaction.reply({ content: "There was an error while executing this command", ephemeral: true })
            .catch(console.error);
    }
});

async function changeKarma (user, amount) {
    let usr = await User.findOne({ where: {userId: user.id} });
    if (usr == null) await User.create({ userId: user.id, karma: amount});
    else await usr.update({karma: Sequelize.literal(`karma + ${amount}`) }); 
}

client.on("messageReactionAdd", async (reaction, user) => {
    let karmicImpact = 0;
    if (positive.includes(reaction.emoji.name)) {
        console.log("Add Positive", reaction.emoji.name);
        karmicImpact = 1;
    } else if (negative.includes(reaction.emoji.name)) {
        console.log("Add Negative", reaction.emoji.name);
        karmicImpact = -1;
    } else {
        return;
    }

    changeKarma(reaction.message.author, karmicImpact);
});

client.on("messageReactionRemove", async (reaction, user) => {
    let karmicImpact = 0;
    if (positive.includes(reaction.emoji.name)) {
        console.log("Subtract Positive", reaction.emoji.name);
        karmicImpact = -1;
    } else if (negative.includes(reaction.emoji.name)) {
        console.log("Subtract Negative", reaction.emoji.name);
        karmicImpact = 1;
    } else {
        return;
    }

    changeKarma(reaction.message.author, karmicImpact);
});

// Capute raw packets to get reaction events on uncached messages
client.on("raw", async packet => {
    // Filter for only message reaction events
    if (!["MESSAGE_REACTION_ADD", "MESSAGE_REACTION_REMOVE"].includes(packet.t)) return;

    try {
        // Fetch channel from cache
        let channel = await client.channels.fetch(packet.d.channel_id);

        // Reject messages which have already been cached to stop a double event fire
        if (channel.messages.cache.get(packet.d.message_id)) return;

        // Otherwise fetch message and replace partial with full object
        let message = await channel.messages.fetch(packet.d.message_id);
        packet.d.message = message;

        // If custom emoji use the ID rather than the name. Fetch from reaction cache
        let emoji = packet.d.emoji.id ? packet.d.emoji.id : packet.d.emoji.name;
        let reaction = packet.d.message.reactions.cache.get(emoji);

        // Adds the currently reacting user to the reaction's users collection.
        if (reaction) reaction.users.cache.set(packet.d.user_id, await client.users.fetch(packet.d.user_id));

        // Check which type of event it is before emitting
        // In the case of an error fetching something use the packet data as a fallback
        // "partial reaction"
        if (packet.t === "MESSAGE_REACTION_ADD") {
            client.emit("messageReactionAdd", reaction || packet.d, client.users.cache.get(packet.d.user_id));
        }
        if (packet.t === "MESSAGE_REACTION_REMOVE") {
            client.emit("messageReactionRemove", reaction || packet.d, client.users.cache.get(packet.d.user_id));
        }
    } catch (error) {
        console.error(error);
    }
});

client.once("ready", async () => {
    console.log("CultBot Ready");
    try {
        await sequelize.authenticate();
        console.log("Connected to database");
        await sequelize.sync({ force: true });
        console.log("Synced Database Model");

        client.user.setPresence({ activities: [{ type: "COMPETING", name: "CultBot v2" }], status: "online" });
    } catch (error) {
        console.error("Unable to connect to database:", error);
        process.exit(1);
    }
});

client.login(process.env.DISCORD_TOKEN);