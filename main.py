import os
from discord.ext import commands
from jsonUtils import *

inky = readInJson("classes.json")

bot = commands.Bot(command_prefix=inky["prefix"])

for f in os.listdir('./cogs'):
    if f.endswith('.py'):
        bot.load_extension(f'cogs.{f[:-3]}')


bot.run(inky["token"])
