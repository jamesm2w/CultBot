import discord.ext.commands as commands

ADMIN_ROLE_ID = 782307508261879829
OWNER_ID = 330764682204020737


def admin_command():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID or ctx.guild.get_role(ADMIN_ROLE_ID) in ctx.author.roles
    return commands.check(predicate)
