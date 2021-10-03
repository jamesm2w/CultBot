const { positive, negative } = require("./../emojiConfig.json");

module.exports = {
    get data() {
        return {
            "name": "Karma Impact",
            "type": 3
        };
    },
    async execute(interaction, User) {
        if (interaction.targetType != "MESSAGE") return;
        let channel = await interaction.client.channels.fetch(interaction.channelId);

        let message = await channel.messages.fetch(interaction.targetId);
        
        let impact = 0;
        await message.reactions.cache.each(reaction => {
            console.log(reaction);
            if (positive.includes(reaction.emoji.name)) {
                impact++;
            } else if (negative.includes(reaction.emoji.name)) {
                impact--;
            }
        });

        let karma = await User.findOne({
            where: {
                userId: message.author.id
            }
        });
        if (karma == null) karma = {karma: "no recorded"};


        channel.send({ 
            content: `${interaction.user}: Karma Impact:
This message changed **${message.author.tag}** karma by **${impact}**.
**${message.author.tag}** now has **${karma.karma}** karma.`, 
            reply: { 
                messageReference: interaction.targetId, 
                failIfNotExists: false 
            } 
        });
        
        
        await interaction.reply({ content: "Calculated impact for message below", ephemeral: true});
    }
}