import discord
from discord.ext import tasks, commands
import logging

import sys
sys.path.append('helpers')
from remindHelper import *
from randomImage import *
from solve import *
from randomGame import *

import datetime
import random
import json
import asyncio

#Handle logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Bot setup
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged on as {0.user}!'.format(bot))

#Ping test
@bot.command()
async def ping(ctx):
    await ctx.channel.send('Pong!')

#Gets the current day
@bot.command()
async def date(ctx):
    today = datetime.datetime.now()
    await ctx.channel.send('The current date is: {0.month} / {0.day} / {0.year}'.format(today))

#Gets the events for the next few days
@bot.command()
async def remind(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send('**Here are the current group reminders:**\n```\n' + reminders() + '```')

    elif args[0] == 'add':
        message = ''
        for word in args[1:]:
            message += word + ' '
        addReminder(message)
        await ctx.channel.send('**Recieved reminder!**')

    elif args[0] == 'remove':
        if(len(args) != 2):
            await ctx.channel.send('**Incorrect usage! Proper format is "!remind remove <message id>"**')
        else:
            removeReminder(int(args[1]))
            await ctx.channel.send('**Reminder removed!**')

    else:
        await ctx.channel.send('**Here are the current group reminders:**\n```\n' + reminders() + '```')

#Shows how epic you are
@bot.command()
async def epic(ctx, *args):
    if len(args) > 0:
        epicString = ''
        for word in args[0:]:
            epicString += word + ' '
        await ctx.channel.send('**On the epic scale, I rate ' + epicString + str(random.randint(0, 10)) + ' out of 10**')
    else:
        await ctx.channel.send('**On the epic scale, I rate ' + ctx.author.name + ' ' + str(random.randint(0, 10)) + ' out of 10**')

#Displays a random image from imgur
@bot.command()
async def rimage(ctx):
    await ctx.channel.send(getImage())

#Answers a math equation with 2 integers
@bot.command()
async def solve(ctx, *args):
    if len(args) != 3:
        await ctx.channel.send('**The proper format is *!solve <number1> <sign> <number2>***')
    else:
        await ctx.channel.send('**The answer to your problem is: ' + str(solveInput(int(args[0]), args[1], int(args[2]))) + '**')

#Chooses a random game to play. games.txt
@bot.command()
async def rgame(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send('**You should play: *' + randomGame() + '***')
    elif args[0] == 'add':
        game = ''
        for word in args[1:]:
            game += word + ' '
        addGame(game)
        await ctx.channel.send('**Added game to list!**')
    else:
        await ctx.channel.send('**You should play: *' + randomGame() + '***')

#Plays the vine boom sound effect
@bot.command()
async def vine_boom(ctx, arg1=None):
    if arg1 == 'stop':
        vineBoomLoop.cancel()
        await ctx.channel.send('**Ending Boom Sounds**')
    else:
        vineBoomLoop.start(ctx)
        await ctx.channel.send('**Starting Boom Sounds**')

@tasks.loop(seconds=60.0)
async def vineBoomLoop(ctx):
    await asyncio.sleep(random.randint(0,1800))
    if ctx.voice_client is None:
        channel = ctx.author.voice.channel
    await channel.connect()

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('boom.mp3'))
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    await asyncio.sleep(5)
    await ctx.voice_client.disconnect()

with open('auth.json') as f:
    authJson = json.load(f)
bot.run(authJson['token'])