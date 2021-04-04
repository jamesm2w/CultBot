import discord
import discord.ext.commands as commands
import json

# TODO finish this

UPVOTE = None
DOWNVOTE = None


class Karma(commands.Cog):

    users: dict[int, int]
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
            message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            user_id = message.author.id
            if payload.emoji.id == UPVOTE:
                self.users[user_id] += 1
            elif payload.emoji.id == DOWNVOTE:
                self.users[user_id] -= 1
            self.update_file()

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id is None:
            return
        if payload.emoji.id == DOWNVOTE or payload.emoji.id == UPVOTE:
            message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            user_id = message.author.id
            if payload.emoji.id == UPVOTE:
                self.users[user_id] -= 1
            elif payload.emoji.id == DOWNVOTE:
                self.users[user_id] += 1
            self.update_file()

    def update_file(self):
        with open("data/karma.json", "w+") as f:
            json.dump(self.users, f)

    def load_file(self) -> dict[int, int]:
        try:
            with open("data/karma.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


def setup(bot):
    bot.add_cog(Karma(bot))
