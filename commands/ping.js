const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    get data () {
        return new SlashCommandBuilder().setName("ping").setDescription("Replies with Pong!").toJSON();
    },
    async execute (interaction) {
        await interaction.reply("Pong!");
    }
}