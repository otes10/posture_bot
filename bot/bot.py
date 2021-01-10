import os
import random
import matplotlib.pyplot as plt
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import discord
import json
import requests
import math
from datetime import date
from itertools import cycle
from time import localtime, strftime
from posture_client import get_hourly_report

client = discord.Client()
backgroundTask = None
time = 3600
        
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')

@bot.command(name='start', help='Begins posture monitoring')
async def startProg(ctx):
    response = 'Monitoring posture'
    await ctx.send(response)

@bot.command(name='stop', help='stops posture monitoring')
async def stopProg(ctx):
    response = 'No longer monitoring posture'
    await ctx.send(response)
    global time
    time = math.inf
    asyncio.run(createReportingProcess())

@bot.command(name='currentreport', help='Displays the days report')
async def getRep(ctx):
    response = 'Here is todays report so far'
    await ctx.send(response)
    await retrieveReport()

@bot.command(name='setreporttime', help='set the interval for automatic reports (seconds)')
async def setTime(ctx, arg):
    assert(type(arg=int))
    global time
    time = arg
    global backgroundTask
    if backgroundTask != None:
        backgroundTask.cancel()
    backgroundTask = asyncio.create_task(createReportingProcess())


# @bot.command(name='visualize report', help='Create a graphical visualization for your report')
# async def runProg(ctx):

# async def genVisReport():
#     plt.title('report for {}'.format(strftime("%a, %d %b %Y", localtime)))
#     plt.ylabel('proportion')
#     hours = None
#     left = range(hours * 2)
#     tick_label = ['good', 'bad'] * hours


async def createReportingProcess():
    await client.wait_until_ready()
    while not client.is_closed:
        global time
        asyncio.sleep(time)
        asyncio.run(retrieveReport())


async def retrieveReport():
    data = {'date': '2021_1_10', 'hour':'9'}
    report = get_hourly_report(data)
    for i in report['2021_1_10']:
        good = i['posture']['good']
        print(good)
    

bot.run(TOKEN)