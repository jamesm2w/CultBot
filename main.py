from discord.ext import commands
import apitoken
import discord
import argparse

EXTENSIONS = [
    "cogs.example",
    "cogs.react",
    "cogs.someone",
    "cogs.karma",
]

intents = discord.Intents.default()
intents.members = True


# initalise the bot and load all the selected cogs
bot = commands.Bot(command_prefix="\\", intents=intents)

for ext in EXTENSIONS:
    bot.load_extension(ext)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    token = apitoken.TEST_TOKEN if parser.parse_args().test else apitoken.TOKEN
    bot.run(token)
