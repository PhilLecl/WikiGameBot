#!/usr/bin/env python3
import wikigamebot
from discord.ext import commands
import json

# constants
CONFIG_FILE = "config.json"
SECRETS_FILE = "secrets.json"

if __name__ == "__main__":
    with open(SECRETS_FILE) as sf, open(CONFIG_FILE) as cf:
        secrets = json.load(sf)
        config = json.load(cf)

    bot = commands.Bot(command_prefix=config["command_prefix"])


    @bot.event
    async def on_ready():
        print("Logged in as {0.user}".format(bot))


    bot.add_cog(wikigamebot.WikiGame(bot))
    bot.run(secrets["token"])
