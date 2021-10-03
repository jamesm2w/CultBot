module.exports = {
    get data () {
        return {
            "name": "Karma",
            "type": 2
        };
    },
    async execute (interaction, User) {
        if (interaction.targetType != "USER") return;
        let user = await interaction.client.users.fetch(interaction.targetId);

        let karma = await User.findOne({
            where: {
                userId: user.id
            }
        });

        if (karma == null) karma = {karma: "no recorded"};

        await interaction.reply({ content: `User **${user.username}** currently has **${karma.karma}** karma`});
    }
}