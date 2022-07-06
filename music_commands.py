import asyncio

import discord
import youtube_dl

ytdl_format_options = {
    'format': 'bestaudio',
    'restrictfilenames': True,
    'outtmpl': 'files/%(title)s.mp3',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


class Music:
    async def play(self, message, loop):
        url_list = []
        if not message.author.voice:
            await message.channel.send("{} is not connected to a voice channel".format(message.author.name))
            return
        else:
            channel = message.author.voice.channel
        try:
            await channel.connect()
        except:
            pass

        url = message.content.split(' ')[-1]
        url_list.append(url)
        filename_list = []
        try:
            server = message.guild
            voice_channel = server.voice_client

            filename = await YTDLSource.from_url(url, loop=loop)
            filename_list.append(filename)

            voice_channel.play(discord.FFmpegPCMAudio(source=filename, executable="ffmpeg.exe"))
            await message.channel.send('**Now playing:** {}'.format(filename.title()))

        except Exception as ex:
            print(ex)
            if message.guild.voice_client.is_playing():
                pass
            else:
                await message.channel.send("The bot is not connected to a voice channel.")

    async def stop(self, message):
        voice_client = message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await message.channel.send("The bot is not playing anything at the moment.")

    async def pause(self, message):
        voice_client = message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await message.channel.send("The bot is not playing anything at the moment.")

    async def resume(self, message):
        voice_client = message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await message.channel.send("The bot was not playing anything before this. Use play_song command")

    async def leave(self, message):
        voice_client = message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await message.channel.send("The bot is not connected to a voice channel.")