from discord.ext import commands
from apitoken import TOKEN
import discord

EXTENSIONS = [
    "cogs.example",
    "cogs.react",
    "cogs.praise",
    "cogs.someone"
]

intents = discord.Intents.default()
intents.members = True


# initalise the bot and load all the selected cogs
bot = commands.Bot(command_prefix="\\", intents=intents)

for ext in EXTENSIONS:
    bot.load_extension(ext)

if __name__ == "__main__":
    bot.run(TOKEN)
