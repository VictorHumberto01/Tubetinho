import asyncio
import discord
import yt_dlp
import files
from discord.ext import commands
# Imported all the components needed to make the bot work. The files one is the side script
# used to delete the used files and keep the bot folder clean.

# Change the '+' to your choice if you want
client = commands.Bot(command_prefix='+', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)

yt_dlp.utils.bug_reports_message = lambda: ''


# yt_dlp parameters

yt_dlp_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(yt_dlp_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


queue = []

#Play command
@client.command()
async def play(ctx: object, url) -> object:
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    # Connects to the user channel if not connected to other channel
    channel = ctx.message.author.voice.channel
    if voice is None:
        await channel.connect()
        files

    # Uses the url parameter to add the music to the queue
    global queue

    
    
    
    #checks if the url it's in the queue if not will add it
    try:
        if url not in queue:
            queue.append(url)
        server = ctx.message.guild
        voice_channel = server.voice_client
    except IndexError:
        if queue == []:
            await ctx.send('**Não tem nenhuma musica na fila!**')


    # Will try to play the music with the parameters above
    # If can't send a message to the user chat
    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=client.loop)
            voice_channel.play(player, after=lambda e: print('Error: %s' % e) if e else None)

            await ctx.send('**Tocando agora:** {}'.format(player.title))
            del queue[0]
        
    except Exception as e:
        await ctx.send('**Adicionei a música na lista!**')



@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send('Eu não estou conectado a nenhum canal')


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command(name='queue')
async def queue_(ctx):
    if len(queue) == 1:
        await ctx.send('**Tem {} música na fila!**'.format(len(queue)))
    else:
        await ctx.send('**Tem {} músicas na fila!**'.format(len(queue)))
    await ctx.send('Se quiser limpar a fila use o comando +clear.')

@client.command()
async def skip(ctx):
    await stop(ctx)
    try:
        url = queue[0]
        await play(ctx, url)
    except IndexError:
        await ctx.send('**Não tem nenhuma musica na fila!**')

@client.command()
async def clear(ctx):
    global queue
    await ctx.send('**Limpei a fila!**')
    queue = []
    
#Command used to diagnostics in the queue
#Uncomment with you want to use it

#@client.command()
#async def status(ctx):
#    print(queue)
#    print(len(queue))
#    print(queue[0])



@client.command()
async def next(ctx):
    await stop(ctx)
    url = queue[0]
    await play(ctx, url)

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    if before.channel is None and after.channel is not None:
        return
    if before.channel is not None and after.channel is None:
        voice_client = discord.utils.get(client.voice_clients, guild=member.guild)
        if voice_client is not None and len(before.channel.members) == 1:
            await voice_client.disconnect()

# Copy your bot token in the parentesis
# Do no remove the ''
client.run('TOKEN')