import discord.ext.commands as commands
import discord
from util import admin_command
import json
import re
from typing import Dict

# For now, only supports custom emoji as reactions due to differences in the way
# discord emoji and unicode emoji are handled.
# As a workaround, just add the unicode emoji as a custom emote to the server


class React(commands.Cog):

    reacts: Dict[str, int]

    def __init__(self, bot):
        self.bot = bot
        self.reacts = self.load_reacts()

    @commands.command()
    @admin_command()
    async def addreact(self, ctx, regex: str, emote: discord.Emoji):
        # check the regex is valid
        try:
            re.compile(regex)
        except re.error:
            await ctx.send("Invalid Regex!")
            return

        # check the bot can use the emoji
        if not emote.is_usable():
            await ctx.send("I can't use this emoji. Please try a different one")
            return

        # store the regex in dict
        self.reacts[regex] = emote.id

        # update the json on disk5
        self.update_file()

        await ctx.send("Succesfully saved auto-react!")

    @ commands.Cog.listener("on_message")
    async def do_react(self, message):
        # check if the message matches any of our regexes
        for regex in self.reacts:
            if re.search(regex, message.content):
                # if so, do the reaction
                emoji: discord.Emoji = await message.guild.fetch_emoji(self.reacts[regex])
                await message.add_reaction(emoji)

    def load_reacts(self) -> Dict[str, int]:
        try:
            with open("data/reacts.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def update_file(self):
        with open("data/reacts.json", "w+") as f:
            json.dump(self.reacts, f)


def setup(bot):
    bot.add_cog(React(bot))
