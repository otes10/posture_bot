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
import datetime
from itertools import cycle
from time import localtime, strftime
from posture_client import get_hourly_report
from statistics import mean

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
    response = 'Here is this hours report'
    await ctx.send(response)
    now = datetime.datetime.now()
    await retrieveReport(ctx, now.hour)

@bot.command(name='hourreport', help='set the interval for automatic reports (seconds)')
async def setTime(ctx, arg):
    response = 'Here is the report for {}:00'.format(arg)
    await ctx.send(response)
    hour = arg
    await retrieveReport(ctx, arg)

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


async def retrieveReport(ctx, hour):
    data = {'date': '2021_1_10', 'hour':str(hour)}
    report = get_hourly_report(data)
    good = []
    for i in report['2021_1_10']:
        good.append(i['posture']['good'])
    average = mean(good)
    myStr ="For the hour of {0} on {1} you averaged a {2} score for good posture".format(data['date'], data['hour'], average)
    await ctx.send(myStr)
    
    

bot.run(TOKEN)