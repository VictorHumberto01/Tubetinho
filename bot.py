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

#Isn't the best way to do it but its working
@client.command()
async def play(ctx: object, url) -> object:
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice is None:
        await channel.connect()
        files

    global queue
    queue.append(url)
    server = ctx.message.guild
    voice_channel = server.voice_client

    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=client.loop)
            voice_channel.play(player, after=lambda e: print('Erro: %s' % e) if e else None)

            await ctx.send('**Tocando agora:** {}'.format(player.title))
            del (queue[0])
    
    except:
        url = queue[0]
        await ctx.send('**Adicionei a música na fila!**')
        print('test')
        queue.append(url)
        del (queue[0])


    if voice.is_connected():
        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=client.loop)
            voice_channel.play(player, after=lambda e: print('Erro: %s' % e) if e else None)

        await ctx.send('**Tocando agora:** {}'.format(player.title))
        del (queue[0])



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
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` adicionado à fila!')

@client.command()
async def skip(ctx):
    await stop(ctx)
    url = queue[0]
    await play(ctx, url)
    print(queue)



@client.command()
async def next(ctx):
    await ctx.send('**Para pular use o comando skip!**')


# Not working gonna fix later.
async def on_voice_state_update(self, member, before, after, ctx):
    voice = after.channel.guild.voice_client
    if not member.id == self.bot.user.id:
        await voice.disconnect()
        await ctx.send('**O canal estava vazio por isso me desconectei.**')

    elif before.channel is None:
        time = 0
        while True:
            await asyncio.sleep(1)
            time = time + 1
            if voice.is_playing() and not voice.is_paused():
                time = 0
            if time == 600:
                await voice.disconnect()
                await ctx.send('**Me desconectei do canal por conta de inatividade.**')
            if not voice.is_connected():
                break


client.run('TOKEN')
