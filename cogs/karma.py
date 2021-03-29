import discord
import discord.ext.commands as commands
from typing import Dict
import json

UPVOTE = None
DOWNVOTE = None  # brendan plz


class Karma(commands.Cog):

    users: Dict[int, int]
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot
        self.users = self.load_file()

    # get credit @user

    # get top users

    # get bottom users

    # track reacts for +/- credits for that user
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id is None:
            return
        if payload.emoji.id == DOWNVOTE or payload.emoji.id == UPVOTE:
            channel: discord.TextChannel = await self.bot.fetch_channel(payload.channel_id)
            message: discord.Message = await channel.get_partial_message(payload.message_id).fetch()
            user: discord.User = await message.author
            if payload.emoji.id == UPVOTE:
                pass
            elif payload.emoji.id == DOWNVOTE:
                pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        pass

    def update_file(self):
        with open("data/karma.json", "w+") as f:
            json.dump(self.users, f)

    def load_file(self) -> Dict[int, int]:
        try:
            with open("data/karma.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


def setup(bot):
    bot.add_cog(Karma(bot))
