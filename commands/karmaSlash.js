const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    get data() {
        return new SlashCommandBuilder()
            .setName("karma")
            .setDescription("Get a users karma")
            .addUserOption(option =>
                option.setName("target")
                    .setDescription("The user to get karma for")
                    .setRequired(false)
            )
            .toJSON();
    },
    async execute(interaction, User) {
        let target = interaction.options.getUser("target");

        if (target == null) target = interaction.user;

        let karma = await User.findOne({
            where: {
                userId: target.id
            }
        });

        if (karma == null) karma = {karma: "no recorded"};

        await interaction.reply({ content: `User **${target.username}** currently has **${karma.karma}** karma`});
    }
}