import asyncio
import discord
import yt_dlp
import files
from discord.ext import commands
from youtube_search import YoutubeSearch
import re

# Imported all the components needed to make the bot work. The files one is the side script
# used to delete the used files and keep the bot folder clean.

#
bot = discord.Bot()

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

def search_and_get_url(title):
    results = YoutubeSearch(title , max_results=1).to_dict()
    for v in results:
        h = ('https://www.youtube.com' + v['url_suffix'])
        return h



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

global channelstate
global voice_channel
global userchannel
channelstate = False
voice_channel = ''
playing = False
userchannel = ()
queue = []

#Play command
@bot.command(description='Toca uma música')
async def play(ctx: object, *, query: str):
    global channelstate
    global userchannel
    global playing
    if channelstate == True:
        if ctx.author.voice.channel != userchannel:
            return
    else:
        pass
    #Check if the query is a valid URL
    match = re.match("https?://(www\.)?youtube\.com/watch\?v=\S+", query)
    try:
        if match:
            url = query
            pass
        else:
            url = search_and_get_url(query)  
            pass
    except TypeError:
        await ctx.send('**Não consegui tocar a sua música.**')  
        
        
        
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
    # Connects to the user channel if not connected to other channel
    channel = ctx.author.voice.channel
    if channelstate == False:
        await channel.connect()
        userchannel = channel
        channelstate == True
        files
    else:
        pass

    #checks if the url it's in the queue if not will add it
    try:
        if url not in queue:
            queue.append(url)
    except IndexError:
        if queue == []:
            await ctx.respond('**Não tem nenhuma musica na fila!**')


    # Will try to play the music with the parameters above
    # If can't send a message to the user chat
    try:
        global player
        server = ctx.guild
        voice_channel = server.voice_client
        player = await YTDLSource.from_url(queue[0], loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Error: %s' % e))

        await ctx.respond('**Tocando agora:** {}'.format(player.title))
        del queue[0]
        channelstate = True
    except Exception as e:
        await ctx.respond('**Coloquei a música na fila!**')
        
            
    



@bot.command(description='Remove o bot da call')
async def leave(ctx):
    global channelstate
    global voice_channel
    global userchannel
    global queue
    global playing
    
    if channelstate == True:
        if ctx.author.voice.channel != userchannel:
            return
    else:
        pass

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    
    
    if voice.is_connected():
        await voice.disconnect()
        channelstate = False
        voice_channel = ''
        playing = False
        userchannel = ()
        queue = []
    else:
        await ctx.respond('Eu não estou conectado a nenhum canal')


@bot.command(description='Para a música')
async def stop(ctx):
    global channelstate
    global userchannel
    
    if channelstate == True:
        if ctx.author.voice.channel != userchannel:
            return
    else:
        pass
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.respond('⏸︎')

    


@bot.command(description='Mostra quantas músicas estão na fila')
async def queue_(ctx):
    global channelstate
    global userchannel
    
    if channelstate == True:
        if ctx.author.voice.channel != userchannel:
            return
    else:
        pass
    if len(queue) == 1:
        await ctx.respond('**Tem {} música na fila!**'.format(len(queue)))
    else:
        await ctx.respond('**Tem {} músicas na fila!**'.format(len(queue)))

@bot.command(description='Pula a música')
async def skip(ctx):
    global channelstate
    global userchannel
    global queue
    global player

    if channelstate == True:
        if ctx.author.voice.channel != userchannel:
            return
    player = ''
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.invoke(bot.get_command('play'), query=queue[0])


@bot.command(description='Limpa a fila')
async def clear(ctx):
    global queue
    await ctx.respond('**Limpei a fila!**')
    queue = []
    
#Command used to diagnostics in the queue
#Uncomment with you want to use it

#@bot.command()
#async def status(ctx):
#    await ctx.respond(queue)
#    await ctx.respond(len(queue))
#   await ctx.respond(queue[0])



#Add a function that makes the bot exit a channel if it's alone.
@bot.event
async def on_voice_state_update(member, before, after):
    global channelstate
    global voice_channel
    global userchannel
    global queue
    global playing

    if member.bot:
        return
    if before.channel is None and after.channel is not None:
        return
    if before.channel is not None and after.channel is None:
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if voice_client is not None and len(before.channel.members) == 1:
            await voice_client.disconnect()
            channelstate = False
            voice_channel = ''
            playing = False
            userchannel = ()
            queue = []



# Copy your bot token in the parentesis
# Do no remove the ''
bot.run("TOKEN")