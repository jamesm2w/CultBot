from typing import Optional, Union
import discord.ext.commands as commands
import discord
import asyncio
import time

from util import admin_command

DEFAULT_BAN_MSG = "You have been cast out of the cult!"


class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.muted_users: dict[discord.User, Union[None, float]] = {}

    @commands.command()
    @admin_command()
    async def mute(self, ctx: commands.Context, user: discord.Member, bantime: Optional[int]):
        # cant mute bot
        if user.id == self.bot.user.id:
            await ctx.reply("nice try")
            return
        # cant mute self
        if user.id == ctx.author:
            await ctx.reply("why are you trying to mute yourself")
            return
        # cant mute already muted
        if user.id in self.muted_users:
            await ctx.reply("User already muted!")
            return

        # send ban message
        if bantime is None:
            await ctx.reply(f"{user.mention} has been muted forever")
        else:
            await ctx.reply(f"{user.mention} has been muted for {bantime} minutes ")

        # add to muted users dict
        # time is the time at which mute expires
        self.muted_users[user] = None if bantime is None else (time.time() + bantime * 60)

        if bantime is not None:
            await asyncio.sleep(bantime * 60)
            self.muted_users.pop(user)

    # unmute a user
    @commands.command()
    @admin_command()
    async def unmute(self, ctx: commands.Context, user: discord.Member):
        if user not in self.muted_users:
            await ctx.reply("User is not currently muted!")
        else:
            self.muted_users.pop(user)
            await ctx.reply("User has been unmuted.")

    # sends an embed showing all muted users
    @commands.command()
    async def muted(self, ctx: commands.Context):
        embed: discord.Embed = discord.Embed(title="Muted Users", color=0x8b01e6)

        if self.muted_users == {}:
            embed.add_field(name="No users are currently muted.", value="Looks like everyones behaving for now.", inline=True)
        else:
            for user, bantime in self.muted_users.items():

                if bantime is None:
                    time_remaining = "Muted Indefinitely"
                else:
                    time_remaining = self.timestamp(bantime - time.time()) + " remaining."

                embed.add_field(name=user.name, value=time_remaining, inline=True)

        await ctx.send(embed=embed)

    # listener to delete messages from muted users
    @ commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author in self.muted_users.keys():
            await msg.delete()

    def timestamp(self, timedif: float) -> str:
        hrs = int(timedif // 3600)
        mins = int(timedif // 60) - hrs * 60
        secs = int(timedif) - hrs * 3600 - mins * 60
        return f"{hrs}:{mins}:{secs}"


def setup(bot):
    bot.add_cog(Mute(bot))
