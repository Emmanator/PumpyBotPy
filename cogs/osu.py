import os

import discord
from ossapi import Ossapi
from discord.ext import commands
from discord.ext.commands import Context

host = "https://osu.ppy.sh/"
client_id = os.getenv("CLIENT")
client_secret = os.getenv("SECRET")
api = Ossapi(client_id=client_id, client_secret=client_secret)


class Osu(commands.Cog, name="osu"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="osutestcommand",
        description="This is a testing command for osu.",
    )
    async def lookup(self, context: Context, username: str) -> None:
        try:
            user = api.user(username)
        except ValueError as ve:
            await context.send('could not find a user under that name', ephemeral=True)
            return
        embed = discord.Embed(
            title=user.username
        )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Osu(bot))
