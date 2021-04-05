import discord.ext.commands as commands

OWNER_ID = 330764682204020737


def admin_command():
    async def predicate(ctx: commands.Context):
        return ctx.author.id == OWNER_ID or ctx.author.guild_permissions.administrator
    return commands.check(predicate)
