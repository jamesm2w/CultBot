import discord.ext.commands as commands


class Example(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hi there {ctx.author.mention}")


def setup(bot):
    bot.add_cog(Example(bot))
