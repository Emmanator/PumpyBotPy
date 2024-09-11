import requests
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class Danbooru(commands.Cog, name="danbooru"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="danbooru",
        description="Returns an image from danbooru",
    )
    async def danbooru(self, context: Context, tags: str = 'femboy', rating: str = 'e') -> None:
        await context.defer()
        if not context.channel.is_nsfw():
            embed = discord.Embed(
                title="This command is only for NSFW channels."
            )
            embed.set_image(url="https://media1.tenor.com/m/iDdGxlZZfGoAAAAC/powerful-head-slap.gif")
            await context.send(embed=embed, delete_after=5)
            return
        else:
            tags.replace(' ', '+')
            for i in range(5):
                link = f'https://danbooru.donmai.us/posts/random.json?tags={tags}+rating:{rating}'
                response = requests.get(link)
                data = response.json()
                print(data)
                if len(data) > 0 and 'file_url' in data:
                    await context.send(f'Artist: **{data["tag_string_artist"]}** \n'
                                       f'{data["file_url"]}')
                    return
                if data['success'] is False:
                    await context.send('no image found with that tag', delete_after=2)
                    return
                await asyncio.sleep(2)
            await context.send('End of the line, could not find an image', ephemeral=True)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Danbooru(bot))
