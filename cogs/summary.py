import logging
import re
import os
import spacy
from collections import defaultdict, deque
from functools import partial

import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Context

try:
    import markovify
except ImportError:
    logging.warning("Markovify could not be imported xd")

nlp = spacy.load("en_core_web_sm")


def word_split(sentence):
    return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]


def word_join(words):
    sentence = " ".join(word.split("::")[0] for word in words)
    return sentence


class Summary(commands.Cog, name="summary"):
    stored_messages = defaultdict(partial(deque, maxlen=10000))

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name='summary',
        description='does something'
    )
    async def summary(self, context: Context, phrase: str = None):
        await context.defer()
        # channel = discord.utils.get(context.guild.text_channels)
        # print(context.channel.id)
        try:
            with open(f"Functions/{context.channel.id}.txt", 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            await context.send('cannot find a dataset for this channel')
            return

        # print('a')
        markovify_model = markovify.NewlineText(text)
        if phrase is None:
            sentence = markovify_model.make_sentence(tries=1000)
        else:
            try:
                sentence = markovify_model.make_sentence_with_start(phrase, strict=False)
            except markovify.text.ParamError:
                sentence = markovify_model.make_sentence(tries=1000)

        await context.send(f'{sentence}')

    @commands.command(
        name='downloadmsg',
        description='does something'
    )
    @commands.is_owner()
    async def download(self, context: Context, ch: str):
        print("we're doing stuff")
        try:
            ch = discord.utils.get(context.guild.channels, id=context.channel.id)
        except AttributeError:
            await context.send(f'No channel with that name found')

        msg = [message async for message in ch.history(limit=100000)]
        msg_content_lst = []
        for m in msg:
            if not m.attachments or m.embeds:
                msg_content_lst.append(m.content)

        # This line cleans up text, removing any special characters so it can be used.
        msg_content_lst_trim = [re.sub(r"\b(?:https?|ftp)://\S+|<[^>]+>", '', i) for i in msg_content_lst]
        msg_file_exists = os.path.isfile(f'Functions/{context.channel.id}.txt')
        msg_file = open(f'Functions/{ch.id}.txt', 'a' if msg_file_exists else 'w', encoding='utf-8')
        for i in msg_content_lst_trim:
            if len(i) > 0:
                msg_file.write(f'{i}\n')
        print("we're done")


async def setup(bot) -> None:
    await bot.add_cog(Summary(bot))
