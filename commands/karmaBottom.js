const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed } = require("discord.js");

module.exports = {
    get data() {
        return new SlashCommandBuilder()
            .setName("bottomkarma")
            .setDescription("Get top users by karma")
            .toJSON();
    },
    async execute(interaction, User) {

        let description = async () => {
            let users = await User.findAll({
                order: [ ["karma", "ASC"] ]
            });
            let lines = [];
            for (let user of users) {
                let discordUser = await interaction.client.users.fetch(user.userId);
                lines.push(`${discordUser.tag} : ${user.karma}`);
            }

            return Promise.all(lines);
        }

        let desc = await description();

        if (desc.length > 10) {
            desc = desc.slice(10);
        }

        if (desc.length == 0) {
            desc = "No users have any karma";
        } else {
            desc = desc.join("\n");
        }

        await interaction.reply({ embeds: [
            new MessageEmbed().setColor("#8b01e6")
            .setTitle("Top 10 Users by Karma")
            .setDescription(desc)
        ] });
    }
}