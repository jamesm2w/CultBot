import discord.ext.commands as commands
import discord.ext.tasks as tasks
import random

CHANNEL_ID = 798498042818330624
GUILD_ID = 763710886052495360


class Birthday(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.birthday.start()

    def cog_unload(self) -> None:
        self.birthday.cancel()

    @tasks.loop(hours=12)
    async def birthday(self):
        if(random.randint(0, 5) == 0):
            await self.wish_happy_birthday()

    async def wish_happy_birthday(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        user = random.choice(self.bot.get_guild(GUILD_ID).members)
        await channel.send(f"It is {user.mention}'s birthday today! Be sure to wish {user.mention} a happy birthday!")
        await channel.send("🥳")


def setup(bot):
    bot.add_cog(Birthday(bot))
