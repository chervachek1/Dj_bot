import discord
import os
from music_commands import Music
import youtube_dl
from dotenv import load_dotenv
load_dotenv(fr'C:\CONFIG.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
youtube_dl.utils.bug_reports_message = lambda: ''


class MyClient(discord.Client, Music):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        prefix = '?'
        if message.content.startswith(prefix):
            command = message.content[len(prefix):]
            is_admin = [role.name for role in message.author.roles]

            if command == 'help':
                await message.channel.send("```\n"
                                           "Commands:\n"
                                           "help - This is the help command\n"
                                           "play - play your sound from Youtube link\n"
                                           "pause - audio pause\n"
                                           "resume - resume audio\n"
                                           "stop - stop audio\n"
                                           "stats - check the stats(only for admin)\n"
                                           "more command coming soon\n"
                                           "```")

            elif command == 'stop':
                await self.stop(message)

            elif 'play' in command:
                await self.play(message, loop=client.loop)

            elif command == 'pause':
                await self.pause(message)

            elif command == 'resume':
                await self.resume(message)

            elif command == 'leave':
                await self.leave(message)

            elif command == 'stats' and "Admin" in is_admin:
                await message.channel.send('Hello Admin!')

            else:
                await message.channel.send("```\n"
                                           "This command doesn't exist\n"
                                           "Use the '?help' command to see all available commands!\n"
                                           "```")


client = MyClient()
client.run(DISCORD_TOKEN)
