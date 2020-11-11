from discord.ext import commands, tasks
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from jsonUtils import *
from datetime import datetime


class listeners(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.place = 0
        self.inky = readInJson("classes.json")
        self.inky_length = len(self.inky["classes"])
        self.DM = self.inky["DM"]
        self.CHANNEL = self.inky["CHANNEL"]
        self.remind_channel = self.inky["channelID"]

    async def inky_remind(self):
        print("Remind Triggered")
        inky_classes = self.inky["classes"]

        class_name = inky_classes[self.place % self.inky_length]['name']
        class_url = inky_classes[self.place % self.inky_length]['url']
        class_text = inky_classes[self.place % self.inky_length]['text']

        embed = discord.Embed(title=class_name, url=class_url, description=class_text, color=discord.Colour.blue())

        user = await self.bot.fetch_user(self.inky["discordID"])
        if self.DM:
            await user.send(embed=embed)
        if self.CHANNEL:
            channel = await self.bot.fetch_channel(self.inky["channelID"])
            await channel.send(f"{user.mention}\n", embed=embed)

        self.place += 1

    @commands.Cog.listener()
    async def on_ready(self):
        for i in range(self.inky_length):
            time = self.inky["classes"][i]["time"]
            hour, minute = time.split(":")
            self.scheduler.add_job(self.inky_remind, CronTrigger(hour=hour, minute=minute, day_of_week="MON-FRI"))
        self.scheduler.start()

        print("Bot now online")

    @commands.Cog.listener()
    async def on_disconnect(self):
        print("Bot Offline")

    @commands.command()
    async def reload(self, ctx: commands.Context):
        self.scheduler.remove_all_jobs()
        for i in range(self.inky_length):
            time = self.inky["classes"][i]["time"]
            hour, minute = time.split(":")
            self.scheduler.add_job(self.inky_remind, CronTrigger(hour=hour, minute=minute, day_of_week="MON-FRI"))
        await ctx.send("Reloaded scheduler")
        print("Reloaded classes")

    @commands.command(aliases=["n"])
    async def next(self, ctx: commands.Context):
        await ctx.trigger_typing()
        now = datetime.now().strftime("%H:%M")
        n_hour, n_minute = now.split(":")
        n_hour = int(n_hour)
        n_minute = int(n_minute)

        next_class_time = self.inky["classes"][self.place % self.inky_length]["time"]
        i_hour, i_minute = next_class_time.split(":")
        i_hour = int(i_hour)
        i_minute = int(i_minute)

        remaining_minutes = ((i_hour - n_hour) * 60) + (i_minute - n_minute)
        
        if remaining_minutes < 0:
            remaining_minutes += 1440

        await ctx.send(f"{remaining_minutes} minutes until {self.inky['classes'][self.place % self.inky_length]['name']}")


def setup(bot: commands.Bot):
    bot.add_cog(listeners(bot))
