import os

import discord
from ossapi import Ossapi
from discord.ext import commands
from discord.ext.commands import Context

client_id = os.getenv("CLIENT")
client_secret = os.getenv("SECRET")

print(client_id)
print(client_secret)