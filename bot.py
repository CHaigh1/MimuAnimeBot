import discord
from discord.ext import tasks, commands
import logging

import sys
sys.path.append('helpers')
from remindHelper import *
from randomImage import *
from solve import *
from randomGame import *
from pornCount import *
from YTDLSource import *
from anime import *

import datetime
import random
import json
import asyncio
import re
import os

#Handle logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Bot setup
bot = commands.Bot(command_prefix=('!', '.'), intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Logged on as {0.user}!'.format(bot))

#List all commands
@bot.command()
async def commands(ctx):
    commandList = '!ping\n!date\n!remind <empty/add/remove> <arg>\n!epic <empty/arg>\n!rimage\n!solve\n!rgame <empty/add>\n!vine_boom <empty/stop>'
    await ctx.channel.send('**The commands are:**\n```' + commandList + '```')

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
    else:
        channel = ctx.author.voice.channel

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('boom.mp3'))
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    await asyncio.sleep(5)
    await ctx.voice_client.disconnect()

#Counts the number of times user has gotten porn from !rimage
@bot.command()
async def porn(ctx, *args):
    if len(args) > 0 and args[0] == 'count':
        await ctx.channel.send('**Here are the total times porn has been posted from !rgame:**\n```\n' + countPorn() + '```')
    else:
        addPorn(ctx.author.name)
        await ctx.channel.send('Wow **' + ctx.author.name + '** just found porn! Adding 1 to the counter\nhttps://cdn.discordapp.com/attachments/941145618527698944/947652329803509820/thirsty.mp4')

#How to start music. Uses YT links/search or SoundCloud
#TODO: add playlists
@bot.command()
async def play(ctx, *args):
    channel = ctx.author.voice.channel
    song = ''
    for word in args:
        song = song + word + ' '

    if ctx.voice_client is None:
        await channel.connect()     

    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        return

    if not ctx.voice_client.is_playing():
        if '&list' in song:
            song = await YTDLSource.from_playlist(song)
        source = await YTDLSource.from_url(song)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else asyncio.run(playNextSong(ctx)))
        await on_voice_state_update(ctx)
    else:
        song_title = YTDLSource.get_title(song)
        YTDLSource.add_song(song, song_title)
        await ctx.channel.send('Adding song to queue. Queue position: ' + str(len(YTDLSource.get_queue())))

#Plays the next song in queue. To be used in play()
async def playNextSong(ctx):
    if len(YTDLSource.get_queue()) == 0:
        return

    await asyncio.sleep(1)
    songLink = YTDLSource.pop_queue()
    source = await YTDLSource.from_url(songLink['url'])
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else asyncio.run(playNextSong(ctx)))

#Waits 5 minutes of inactivity then disconnects if nothing is playing
async def on_voice_state_update(ctx):
    voice = ctx.voice_client
    time = 0
    while True:
        await asyncio.sleep(1)
        time = time + 1
        if voice.is_playing() or voice.is_paused():
            time = 0
        if time == 300:
            await voice.disconnect()
        if not voice.is_connected():
            return

#Pauses the currently playing song
@bot.command()
async def pause(ctx):
    if not ctx.voice_client.is_paused():
        ctx.voice_client.pause()

#Stops the current song and disconnects bot
@bot.command()
async def stop(ctx):
    if ctx.voice_client.is_paused() or ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    #os.remove('.\\ytcache\\*')

#Skips song currently playing
@bot.command()
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await playNextSong(ctx)

@bot.command()
async def queue(ctx):
    num_queue = len(YTDLSource.get_queue())
    song_queue = YTDLSource.get_queue()

    if num_queue == 0:
        await ctx.channel.send('There are currently no songs in queue. Add some more!')
    else:
        next_song_count = 3
        if num_queue < next_song_count:
            next_song_count = num_queue

        next_songs = ''
        for song in song_queue[:3]:
            next_songs = next_songs + song['title'] + '\n'

        await ctx.channel.send('There are currently **' + str(num_queue) + '** songs in queue. Here are the next ' + str(next_song_count) + ' songs in queue:' + \
        '```' + next_songs + '```')

@bot.command()
async def shuffle(ctx):
    if len(YTDLSource.get_queue()) > 0:
        YTDLSource.shuffle_queue()
        await ctx.channel.send('Queue shuffled.')
    else:
        await ctx.channel.send('Nothing is currently in the queue')

#Searches for random anime. Thanks Nathan for the code :^)
@bot.command()
async def ranime(ctx, *args):
    if (len(args) > 0 and args[0] == 'bad'):
        await ctx.channel.send(randomAnime(badAnime=True))
    elif (len(args) > 0 and args[0] == 'good'):
        await ctx.channel.send(randomAnime(goodAnime=True))
    else:
        await ctx.channel.send(randomAnime())

#TO ADD
#Anime command
#SQL support?

with open('auth.json') as f:
    authJson = json.load(f)
bot.run(authJson['token'])