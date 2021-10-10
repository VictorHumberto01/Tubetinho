import asyncio
import discord
from discord.ext import commands
import yt_dlp

#Prefixo do bot
client = commands.Bot(command_prefix='+')

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

@client.command(name='play', help='This command plays songs')
async def play(ctx: object) -> object:
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    if voice is None:
        await channel.connect()

    global queue
    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Erro: %s' % e) if e else None)

    await ctx.send('**Tocando agora:** {}'.format(player.title))
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
    await play(ctx)



@client.command()
async def remove(ctx, number):
    global queue

    try:
        del (queue[int(number)])
        await ctx.send(f'Sua fila agora está `{queue}!`')

    except:
        await ctx.send('A fila esta vazia!')

@client.command()
async def ninfetinha(ctx):
    await ctx.send('Gustavo, eu sei que você está na puberdade mas eu sou apenas um bot, por favor mantenha isso somente para você.')
    await ctx.send('Assinado: **Tubetinho**')

@client.command()
async def next(ctx):
    await ctx.send('**Para pular use o comando skip!.**')






@commands.Cog.listener()
async def on_voice_state_update(self, member, before, after, ctx):
    if not member.id == self.bot.user.id:
        return

    elif before.channel is None:
        voice = after.channel.guild.voice_client
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

