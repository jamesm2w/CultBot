from typing import Optional

from discord import message
from util.checks import no_general
import discord
import discord.ext.commands as commands
import json
import discord.ext.tasks as tasks
from random import randint
import asyncio


# the emojis configured for altering karma
# PR if anyone wants to change

UPVOTES = [
    814600173287243796  # :thistbh:
    , 797954796682346526  # :mikepog:
    , 783792678751436830  # :leopog:
    , 763731230339366922  # :matt:
    , 775423225400262656  # :kekw:
    , 834165255390101554  # :salute:
    , 819251214877065267  # :pog:

]
DOWNVOTES = [
    770970521566445599  # :notthistbh:
    , 775670477397032961  # :mikeangry:
    , 793614239641239604  # :skiros:
    , 805047782716342282  # :sus:
]


class Karma(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.users: dict[int, int] = self.load_file()
        self.modified = True
        self.write.start()

    # get credit @user
    @commands.command()
    async def karma(self, ctx: commands.Context, user: Optional[discord.Member]):
        if user is None:
            user = ctx.author
        if user.id in self.users:
            await ctx.reply(f"User {user.name} currently has {self.users[user.id]} karma")
        else:
            await ctx.reply(f"User {user.name} currently has 0 karma")

    # get top users
    @commands.command()
    async def topkarma(self, ctx: commands.Context):
        topten: list[int] = sorted(self.users.keys(), key=lambda x: self.users[x], reverse=True)[:10]

        message = "\n".join([f"{await self.bot.fetch_user(usrid)} : {self.users[usrid]}" for usrid in topten])
        embed: discord.Embed = discord.Embed(title="Top 10 Users by Karma", description=message, color=0x8b01e6)
        await ctx.reply(embed=embed)

    # get bottom users
    @commands.command()
    async def bottomkarma(self, ctx: commands.Context):
        bottomten: list[int] = sorted(self.users.keys(), key=lambda x: self.users[x])[:10]
        message = "\n".join([f"{await self.bot.fetch_user(usrid)} : {self.users[usrid]}" for usrid in bottomten])
        embed: discord.Embed = discord.Embed(title="Bottom 10 Users by Karma", description=message, color=0x8b01e6)
        await ctx.reply(embed=embed)

    # track reacts for +/- credits for that user

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id is None:
            return
        if payload.emoji.id in UPVOTES or payload.emoji.id in DOWNVOTES:
            message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            user_id = message.author.id
            if(message.author.id == payload.user_id):
                return
            if payload.emoji.id in UPVOTES:
                self.upvote(user_id)
            elif payload.emoji.id in DOWNVOTES:
                self.downvote(user_id)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id is None:
            return
        if payload.emoji.id in UPVOTES or payload.emoji.id in DOWNVOTES:
            message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            user_id = message.author.id
            if(message.author.id == payload.user_id):
                return
            if payload.emoji.id in UPVOTES:
                self.downvote(user_id)
            elif payload.emoji.id in DOWNVOTES:
                self.upvote(user_id)

    def upvote(self, user: int):
        if user in self.users:
            self.users[user] += 1
        else:
            self.users[user] = 1
        self.modified = True

    def downvote(self, user: int):
        if user in self.users:
            self.users[user] -= 1
        else:
            self.users[user] = -1
        self.modified = True

    def update_file(self):
        with open("data/karma.json", "w+") as f:
            json.dump(self.users, f)

    # load the file into memory from disk
    def load_file(self) -> dict[int, int]:
        try:
            with open("data/karma.json", "r") as f:
                return {int(k): v for (k, v) in json.load(f).items()}
        except FileNotFoundError:
            return {}

    # mutes a user for a random amount of time
    async def mute(self, message: discord.Message):
        self.muted.append(message.author)
        time = randint(20, 300)
        await message.reply(f"The people disliked this message so much, you have been muted for {time} seconds.")
        await asyncio.sleep(time)
        self.muted.remove(message.author)
        await message.channel.send(f"{message.author.mention} has been unmuted.")

    # cache the file back to disk every minute or so
    @tasks.loop(seconds=60)
    async def write(self):
        if self.modified:
            self.update_file()


def setup(bot):
    bot.add_cog(Karma(bot))
