const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    get data () {
        return new SlashCommandBuilder().setName("hello").setDescription("Say hello!").toJSON();
    },
    async execute (interaction) {
        await interaction.reply({content: `Hi there ${interaction.user}`});
    }
}