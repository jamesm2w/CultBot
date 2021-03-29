from discord.ext import commands
from apitoken import TOKEN

EXTENSIONS = [
    "cogs.example",
    "cogs.react",
    "cogs.praise"
]


# initalise the bot and load all the selected cogs
bot = commands.Bot(command_prefix="\\")

for ext in EXTENSIONS:
    bot.load_extension(ext)

if __name__ == "__main__":
    bot.run(TOKEN)
