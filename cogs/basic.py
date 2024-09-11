import random

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Basic(commands.Cog, name='basic'):
    def __init__(self, bot) -> None:
        self.bot = bot

    MESSAGE_ROLL = "**{0.display_name}** rolls `{1}`."

    @commands.hybrid_command(
        name='roll',
        description='this command sure does rolls number between 1-100'
    )
    async def roll(self, context: Context) -> None:
        # rolls a random number between 1-100
        rolled = random.randint(1, 100)
        await context.send(self.MESSAGE_ROLL.format(context.message.author, rolled))

    @commands.hybrid_command(
        name='dice',
        description='this command sure does roll dice of various sizes and quantities'
    )
    async def dice(self, context: Context, num: int, sides: int) -> None:
        rolls = []
        for i in range(int(num)):
            rolls.append(random.randint(1, int(sides)))
        await context.send(self.MESSAGE_ROLL.format(context.message.author, f'{num}d{sides} and gets {sum(rolls)}'))

    @commands.hybrid_command(
        name='avatar',
        description="this command sure does display a user's avatar"
    )
    async def avatar(self, context: Context, user: discord.User):
        embed = discord.Embed()
        embed = embed.set_image(url=user.avatar)
        embed.set_author(name=user.display_name, icon_url=user.avatar)
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Basic(bot))
