const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    get data() {
        return new SlashCommandBuilder()
            .setName("google")
            .setDescription("Search Google for something")
            .addStringOption(option => 
                option.setName("query")
                    .setDescription("String to search google with")
                    .setRequired(false)
            )
            .toJSON();
    },
    async execute(interaction) {
        const query = interaction.options.getString("query");
        const url = `https://google.co.uk/` + ((query) ? "search?q=" + query.replace(/ /g, "+") : "");
        await interaction.reply({ content: `<${url}>` });
    }
}