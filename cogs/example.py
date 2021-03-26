import discord.ext.commands as commands


class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hi there {ctx.author.mention}")


def setup(bot):
    # load pickle file from disk
    bot.add_cog(Leaderboard(bot))
