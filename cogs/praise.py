import discord.ext.commands as commands
import discord.ext.tasks as tasks
import random
import discord

CHANNEL_ID = 763722286120566794

MESSAGES = [
    "Amatt"
    # TODO - add some more
]


class Praise(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.send_praise_task.start()

    def cog_unload(self):
        self.send_praise_task.cancel()

    @tasks.loop(minutes=5)
    async def send_praise_task(self):
        # just over every 4 hours, roughly
        if(random.randint(0, 50) == 0):
            await self.send_random_message()

    async def send_random_message(self):
        channel: discord.TextChannel = self.bot.get_channel(CHANNEL_ID)
        msg = random.choice(MESSAGES)
        await channel.send(msg)


def setup(bot):
    bot.add_cog(Praise(bot))
