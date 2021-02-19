# WikiGameBot - a Discord bot for playing a game
# Copyright (C) 2020  Philipp Leclercq
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

import random
import discord
from discord.ext import commands


class WikiGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.submissions = None
        self.channel = None
        self.whitelist = set()
        self.pick = None

    # command checks
    @staticmethod
    async def require_text_channel(ctx):
        if not isinstance(ctx.channel, discord.TextChannel):
            await ctx.send("Games can only be started in text channels.")
            return False
        return True

    @staticmethod
    async def require_dm_channel(ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send("Submissions should be added via a DM. Please pick a new article and submit it privately.")
            return False
        return True

    async def require_game(self, ctx):
        if self.channel is None:
            await ctx.send("There's no game going on right now. Use !start in a text channel to start a game")
            return False
        return True

    async def require_pick(self, ctx):
        if self.pick is None:
            await ctx.send("Please use the 'draw' command to pick an article at random before using this command.")
            return False
        return True

    async def require_game_channel(self, ctx):
        if ctx.channel != self.channel:
            await ctx.send("Please use this command in the game channel only.")
            return False
        return True

    async def require_game_channel_member(self, ctx):
        if ctx.author not in self.channel.members and ctx.author not in self.whitelist:
            await ctx.send("You are not a member of the game channel. What the fuck are you doing?")
            return False
        return True

    async def require_no_pick(self, ctx):
        if self.pick is not None:
            await ctx.send("An article has already been drawn: '{0[1]}'".format(self.pick))
            await ctx.send("You cannot draw or submit an article for now.")
            return False
        return True

    # general functions
    async def show_submitters(self):
        for submission in self.submissions:
            await self.channel.send("  - {0[0].mention}".format(submission))

    async def show_submissions(self):
        for submission in self.submissions:
            await self.channel.send("  - '{0[1]}', submitted by {0[0].mention}".format(submission))

    async def ask_confirmation_new_game(self, ctx):
        await ctx.send("There is currently a game going on:")
        await ctx.send("Server: {0}; Channel: {1}; Submissions: {2}".format(self.channel.guild, self.channel,
                                                                            len(self.submissions)))
        await ctx.send("Are you sure you want to start a new game? This will delete the current game.")
        await ctx.send("Use the 'start' command with the '-f/--force' option to confirm.")

    # bot commands
    @commands.command(aliases=("new",))
    async def start(self, ctx, *args):
        if not await WikiGame.require_text_channel(ctx):
            return
        if self.channel is not None and len(self.submissions) > 0:
            force = len(args) > 0 and (args[0] == "-f" or args[0] == "--force")
            if not force:
                await self.ask_confirmation_new_game(ctx)
                return
            await ctx.send("Deleted old game.")

        self.channel = ctx.channel
        self.pick = None
        self.submissions = set()
        await ctx.send("New game created.")
        await ctx.send("You can now submit articles via the 'submit' command in a DM to me.")

    @commands.command(aliases=("s",))
    async def submit(self, ctx, *_article):
        if not await WikiGame.require_dm_channel(ctx) or not await self.require_game(ctx) \
                or not await self.require_game_channel_member(ctx) or not await self.require_no_pick(ctx):
            return

        article = " ".join(_article)
        if not article or article.isspace():
            await ctx.send("Empty article titles are not allowed.")
            return
        for submission in self.submissions:
            if submission[0] == ctx.author:
                self.submissions.remove(submission)
                await ctx.send("Removed old submission '{0[1]}' by '{0[0]}'".format(submission))
                break
        self.submissions.add((ctx.author, article))
        await ctx.send("Added submission '{0}' by {1.mention}".format(article, ctx.author))

        await self.channel.send("{0.mention} added a submission.".format(ctx.author))
        await self.channel.send(
            "There are now {0} submissions by the following users:".format(len(self.submissions)))
        await self.show_submitters()
        await self.channel.send("Use the 'draw' command to close the submission phase and pick an article at random.")

    @commands.command(aliases=("pick", "random"))
    async def draw(self, ctx):
        if not await self.require_game(ctx) or not await self.require_game_channel(
                ctx) or not await self.require_no_pick(ctx):
            return
        submission = random.choice(tuple(self.submissions))
        self.pick = submission
        await ctx.send("The article is: '{0}'".format(submission[1]))
        await ctx.send("After the interrogation phase, use the 'solution' command to show whose article it was.")

    @commands.command()
    async def solution(self, ctx):
        if self.pick is None:
            await ctx.send("No article has been drawn yet.")
            return
        await self.show_submissions()
        await ctx.send("The drawn article was '{0[1]}', submitted by {0[0].mention}.".format(self.pick))
        self.submissions = set()
        self.pick = None

    @commands.command()
    async def guess(self, ctx):
        mentions = ctx.message.mentions
        if len(mentions) != 1:
            await ctx.send("Guesses are only valid if you mention exactly one user.")
            return
        correct = self.pick[0] in mentions
        await ctx.send("Your guess was {0}.".format("correct" if correct else "wrong"))
        await ctx.send("Use the 'solution' command to show the solution and an overview of all submitted articles.")

    @commands.command()
    async def whitelist(self, ctx):
        if not await self.require_game(ctx) or not await self.require_game_channel(ctx):
            return
        mentions = ctx.message.mentions
        self.whitelist.update(mentions)
        await ctx.send("Added {0} user{1} to the whitelist.".format(len(mentions), ("" if len(mentions) == 1 else "s")))
