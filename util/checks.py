import discord.ext.commands as commands

ADMIN_ROLE_IDS = [782307508261879829, 795358205823549460, 330764682204020737]


def admin_command():
    async def predicate(ctx):
        return ctx.author.id in ADMIN_ROLE_IDS
    return commands.check(predicate)
