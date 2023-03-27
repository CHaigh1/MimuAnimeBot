import discord
import asyncio
import yt_dlp
import queue
import random

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'ytcache\\%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': False,
    'default_search': 'auto',
    'extract_flat': False,
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}


ytdl = yt_dlp.YoutubeDL(ytdl_format_options)
songQueue = queue.Queue()

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        print(data['url'])
        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    @classmethod
    async def from_playlist(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        ytdl_format_options['extract_flat'] = 'in_playlist'
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url))
        ytdl_format_options['extract_flat'] = False

        for song in data['entries'][1:]:
            if type(song) is dict:
                YTDLSource.add_song(song['url'], song['title'])
        data = data['entries'][0]
        first_video_url = data['url']
        return first_video_url

    @classmethod
    async def get_title(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        ytdl_format_options['extract_flat'] = True
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url))
        ytdl_format_options['extract_flat'] = False

        return data['title']

    @classmethod
    def add_song(cls, newLink, title):
        songQueue.put({'url':newLink,'title':title})

    @classmethod
    def get_queue(cls):
        return list(songQueue.queue)

    @classmethod
    def pop_queue(cls):
        return songQueue.get()

    @classmethod
    def shuffle_queue(cls):
        song_list = list(songQueue.queue)
        random.shuffle(song_list)
        songQueue.queue.clear()
        for song in song_list:
            songQueue.put(song)