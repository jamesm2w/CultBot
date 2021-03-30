from typing import Text
import discord
import random
import discord.ext.commands as commands
import discord


class Someone(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cache: dict[discord.TextChannel, list[discord.User]] = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if(message.content.startswith("@someone")):
            user: discord.User = random.choice(await self.get_recent_users(message.channel))
            await message.reply(user.mention)

    async def get_recent_users(self, channel: discord.TextChannel):
        if channel in self.cache.keys():
            return self.cache[channel]
        else:
            users: list[discord.User] = []
            async for msg in channel.history(limit=10000):
                users.append(msg.author)
            self.cache[channel] = users
            return users


def setup(bot):
    bot.add_cog(Someone(bot))
