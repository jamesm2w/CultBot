import discord.ext.commands as commands

OWNER_ID = 330764682204020737
GENERAL_ID = 763710886052495364


def admin_command():
    async def predicate(ctx: commands.Context):
        return ctx.author.id == OWNER_ID or ctx.author.guild_permissions.administrator
    return commands.check(predicate)


def no_general():
    async def predicate(ctx: commands.Context):
        return ctx.channel == 763710886052495364
    return commands.check(predicate)
