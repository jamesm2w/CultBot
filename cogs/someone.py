import discord
import random
import discord.ext.commands as commands


class Someone(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cache: dict[discord.TextChannel, list[discord.User]] = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message.channel, discord.TextChannel):
            raise TypeError

        if(message.content.startswith("@someone")):
            # weighted random choice from authors of last 1k messages
            user: discord.User = random.choice(await self.get_recent_users(message.channel))
            await message.reply(user.mention)

        # DO NOT UNCOMMENT !
        # elif(message.content.startswith("@everyone")):
        #    await message.reply(" ".join(m.mention for m in message.channel.members))

    async def get_recent_users(self, channel: discord.TextChannel):
        if channel in self.cache.keys():
            return self.cache[channel]
        else:
            messages = await channel.history(limit=1000).flatten()
            users = map(lambda m: m.author, messages)

            # cache result for speed
            self.cache[channel] = list(users)
            return users


def setup(bot):
    bot.add_cog(Someone(bot))
