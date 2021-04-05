import discord.ext.commands as commands

ADMIN_ROLE_IDS = [782307508261879829, 795358205823549460]
OWNER_ID = 330764682204020737


def admin_command():
    async def predicate(ctx: commands.Context):
        return ctx.author.id == OWNER_ID or [role.id for role in ctx.author.roles if role.id in ADMIN_ROLE_IDS] != []
    return commands.check(predicate)
