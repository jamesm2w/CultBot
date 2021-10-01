import discord.ext.commands as commands


class Example(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx: commands.Context, *args):
        # no text in command
        if len(args) == 0:
            # if we've replied to something with only the command google the message
            if ctx.message.reference is not None:
                msg: str = ctx.message.reference.cached_message.content
                search_term = msg.replace(" ", "+")
            # otherwise just reply with google home link bc thats dumb
            else:
                await ctx.reply("https://google.co.uk")
                return
        # join the args into a string
        else:
            search_term = "+".join(args)
        # reply
        await ctx.reply(f"https://google.co.uk/search?q={search_term}")


def setup(bot):
    bot.add_cog(Example(bot))
