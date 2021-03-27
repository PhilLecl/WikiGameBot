#!/usr/bin/env python3

# WikiGameBot - a Discord bot for playing a game
# Copyright (C) 2020-2021  Philipp Leclercq
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import wikigamebot
from discord.ext import commands
import json
import sys

# constants
CONFIG_FILE = sys.path[0] + "/config.json"
SECRETS_FILE = sys.path[0] + "/secrets.json"

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
