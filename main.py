from discord.ext import commands
import apitoken
import discord
import os
import argparse

EXTENSIONS = [
    "cogs.example",
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
    parser.add_argument("-e", "--env_token", action="store_true")
    token = apitoken.TOKEN if not parser.parse_args().env_token else os.environ['BOT_TOKEN']
    bot.run(token)
