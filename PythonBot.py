import os
import random
import randfacts
import requests
from io import StringIO as io
import json
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
print('imported all libraries!')
print('trying to connect to discord.')

import discord
from discord.ext import commands

#load_dotenv()
from dotenv import dotenv_values
temp = dotenv_values(".env")
TOKEN = temp('DISCORD_TOKEN')
W2G_TOKEN = temp('W2G_TOKEN')
OWM_TOKEN = temp('OWM_TOKEN')
owm = OWM(OWM_TOKEN)
mgr = owm.weather_manager()

bot = commands.Bot(command_prefix='+')
@bot.event
async def on_ready():
    print('connected and running! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="+help"))
    
@bot.command(name='github', help='Shows you the source-code of this bot')
async def age(ctx):
    response = "https://github.com/Nikurasuu/PythonDiscordBot"
    await ctx.send(response)

@bot.command(name='rolldice', help='Rolls a dice for you (+rolldice [amount] [sides])')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    for _ in range(number_of_dice):
        rolled_number = random.randint(1,number_of_sides)
        await ctx.send(f'rolled: {rolled_number}')

@bot.command(name='isitokay', help="Helps you make decisions, that you can't make.")
async def isitokay(ctx):
    if random.randint(1,2) == 1:
        await ctx.send('Yes it is ٩(◕‿◕｡)۶')
    else:
        await ctx.send('No it is not (｡•́︿•̀｡)')

@bot.command(name='magic', help='Shows you some magic ✧')
async def magic(ctx):
    await ctx.send('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

@bot.command(name='fact', help='Shows you a random fact from the internet ☆ﾐ(o*･ω･)ﾉ')
async def fact(ctx):
    await ctx.send('(⌒ω⌒)ﾉ okay here comes one: ')
    await ctx.send(randfacts.getFact())

@bot.command(name='join', help='joins your channel, so you are not that lonely.')
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send('٩(◕‿◕｡)۶')

@bot.command(name='leave', help='disconnects from your channel.')
async def leave(ctx):
    channel = ctx.author.voice.channel
    await ctx.voice_client.disconnect()
    await ctx.send('(｡•́︿•̀｡)')

@bot.command(name='weather', help='Tells you the weather (+weather [location])')
async def weather(ctx, location: str):
    await ctx.send(f'Das aktuelle Wetter in {location}:')
    observation = mgr.weather_at_place(location)
    w = observation.weather
    temperature = w.temperature('celsius')
    temp = temperature['temp']
    tempmin = temperature['temp_min']
    tempmax = temperature['temp_max']
    await ctx.send(f'Aktuelle Temperatur: {temp} Celsius')
    await ctx.send(f'Heute sind es mindestens {tempmin} Celsius und es werden maximal {tempmax} Celsius!')

@bot.command(name='w2g', help="creates a watch2gether room for you (+w2g [video-link])")
async def w2g(ctx, link=''):
    await ctx.send('creating a room for you:')
    r = requests.post('https://w2g.tv/rooms/create.json', json={"w2g_api_key": W2G_TOKEN, "share": link})
    rdata = json.loads(r.text)
    key = rdata['streamkey']
    url = f'https://w2g.tv/rooms/{key}'
    await ctx.send(url)
    if r.status_code == 500:
        await ctx.send('could not contact the API')

@bot.command(name='me_irl', help='sends a meme from me_irl subreddit')
async def meme(ctx):
    r = requests.get('https://meme-api.herokuapp.com/gimme/me_irl')
    rdata = json.loads(r.text)
    subreddit = rdata['subreddit']
    author = rdata['author']
    await ctx.send(f'I found this on {subreddit} from {author}:')
    await ctx.send(rdata['url'])

@bot.command(name='wholesome', help='sends you a wholesome meme')
async def meme(ctx):
    r = requests.get('https://meme-api.herokuapp.com/gimme/wholesomememes')
    rdata = json.loads(r.text)
    subreddit = rdata['subreddit']
    author = rdata['author']
    await ctx.send(f'I found this on {subreddit} from {author}:')
    await ctx.send(rdata['url'])

@bot.command(name='dank', help='sends you a dank-meme')
async def meme(ctx):
    r = requests.get('https://meme-api.herokuapp.com/gimme/dankmemes')
    rdata = json.loads(r.text)
    subreddit = rdata['subreddit']
    author = rdata['author']
    await ctx.send(f'I found this on {subreddit} from {author}:')
    await ctx.send(rdata['url'])


bot.run(TOKEN)
