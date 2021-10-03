module.exports = {
    get data () {
        return {
            "name": "Karma",
            "type": 2
        };
    },
    async execute (interaction) {
        if (interaction.targetType != "USER") return;
        let user = await interaction.client.users.fetch(interaction.targetId);
        await interaction.reply({ content: `User: ${user.tag}`});
    }
}