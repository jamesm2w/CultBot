from discord.ext import commands
from apitoken import TOKEN
from typing import List

EXTENSIONS = [
    "cogs.example"
]


# initalise the bot and load all the selected cogs
bot = commands.Bot(command_prefix="\\")

for ext in EXTENSIONS:
    bot.load_extension(ext)

if __name__ == "__main__":
    bot.run(TOKEN)
