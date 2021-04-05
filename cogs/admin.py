from typing import Optional
import discord.ext.commands as commands
import discord
import asyncio

from util import admin_command

DEFAULT_BAN_MSG = "You have been cast out of the cult!"


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.muted: list[discord.User] = []

    @commands.command()
    @admin_command()
    async def ban(self, ctx: commands.Context, user: discord.Member, time: Optional[int], reason: Optional[str] = DEFAULT_BAN_MSG):
        await ctx.send(f"{user.mention} has been banned for {'many' if time is None else time} minutes for {'no reason' if reason == DEFAULT_BAN_MSG else reason}")
        await user.ban(reason=reason)
        if time is not None:
            await asyncio.sleep(time * 60)
            await user.unban()

    @commands.command()
    @admin_command()
    async def kick(self, ctx: commands.Context, user: discord.Member, reason: Optional[str] = DEFAULT_BAN_MSG):
        await ctx.send(f"{user.mention} has been kicked for {'no reason' if reason == DEFAULT_BAN_MSG else reason}")
        await user.kick(reason=reason)

    @commands.command()
    @admin_command()
    async def mute(self, ctx: commands.Context, user: discord.Member, time: Optional[int]):
        await ctx.send(f"{user.mention} has been muted for {'many' if time is None else time} minutes ")
        self.muted.append(user)
        if time is not None:
            await asyncio.sleep(time * 60)
            self.muted.remove(user)

    # listener to delete messages from muted users
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author in self.muted:
            await msg.delete()


def setup(bot):
    bot.add_cog(Admin(bot))
