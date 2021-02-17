import os
import random
import randfacts
import requests
from datetime import datetime
from io import StringIO as io
import json
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import mysql.connector
import time
print('imported all libraries!')
print('trying to connect to discord.')

import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
W2G_TOKEN = os.getenv('W2G_TOKEN')
OWM_TOKEN = os.getenv('OWM_TOKEN')
owm = OWM(OWM_TOKEN)
mgr = owm.weather_manager()

mydb = mysql.connector.connect(
    host='localhost',
    user="Maki",
    passwd="Maki",
    database="PythonBot"
)

print(mydb)

connectedServers = 0

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='m!', help_command = help_command)
playingStatus='m!help'
#print('!work-in-progress!')


def debug(ctx):
    dateTimeObj = datetime.now()
    user = ctx.author.id
    username = ctx.author.name
    print(f'{dateTimeObj}: responding {username}({user})')

def getBalance(discordid):
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f'SELECT balance FROM Users WHERE discord_id = {discordid}')
    mydb.commit()
    return mycursor.fetchone()[0]

def getCreationDate(discordid):
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f'SELECT date_joined FROM Users WHERE discord_id = {discordid}')
    mydb.commit()
    date_joined = mycursor.fetchone()[0]
    return datetime.fromtimestamp(date_joined).strftime('%d-%m-%Y')

def getUserID(discordid):
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f'SELECT id FROM Users WHERE discord_id = {discordid}')
    mydb.commit()
    return mycursor.fetchone()[0]


@bot.event
async def on_ready():
    print('connected and running!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=playingStatus))
    activeservers = bot.guilds
    for guild in activeservers:
        #print(guild.name)
        global connectedServers
        connectedServers += 1
    print(f'currently connected to: {connectedServers} servers!')

    
@bot.command(name='github', help='Shows you the source-code of this bot')
async def github(ctx):
    debug(ctx)
    await ctx.send('https://github.com/Nikurasuu/PythonDiscordBot')

@bot.command(name='rolldice', help='Rolls a dice for you (rolldice [amount] [sides])')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    debug(ctx)
    if number_of_dice < 6:
        for _ in range(number_of_dice):
            rolled_number = random.randint(1,number_of_sides)
            await ctx.send(f'rolled: `{rolled_number}`')
    else:
        await ctx.send(f'Sorry you can only roll the dice up to `5` times!')

@bot.command(name='isitokay', help="Helps you make decisions, that you can't make.")
async def isitokay(ctx):
    debug(ctx)
    if random.randint(1,2) == 1:
        await ctx.send('Yes it is ٩(◕‿◕｡)۶')
    else:
        await ctx.send('No it is not (｡•́︿•̀｡)')

@bot.command(name='magic', help='Shows you some magic ✧')
async def magic(ctx):
    debug(ctx)
    await ctx.send('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

@bot.command(name='fact', help='Shows you a random fact from the internet ☆ﾐ(o*･ω･)ﾉ')
async def fact(ctx):
    debug(ctx)
    await ctx.send(f'(⌒ω⌒)ﾉ okay here comes one: \n`{randfacts.getFact()}`')

@bot.command(name='weather', help='Tells you the weather (weather [location])')
async def weather(ctx, location: str):
    debug(ctx)
    print('contacting api.openweathermap.org')
    observation = mgr.weather_at_place(location)
    w = observation.weather
    temperature = w.temperature('celsius')
    temp = temperature['temp']
    tempmin = temperature['temp_min']
    tempmax = temperature['temp_max']
    print('success')
    await ctx.send(f'The weather in `{location}`: \nTemperature right now: `{temp}` celsius \nToday are at least `{tempmin}` celsius and it should get up to {tempmax} celsius!')

@bot.command(name='w2g', help="Creates a watch2gether room for you (w2g [video-link])")
async def w2g(ctx, link=''):
    debug(ctx)
    print('contacting w2g.tv/rooms/create.json')
    r = requests.post('https://w2g.tv/rooms/create.json', json={"w2g_api_key": W2G_TOKEN, "share": link})
    if r.status_code == 500:
        await ctx.send('could not contact the API')
        print('could not contact the API')
    else:
        rdata = json.loads(r.text)
        key = rdata['streamkey']
        url = f'https://w2g.tv/rooms/{key}'
        await ctx.send(f'I created a room for you:\n{url}')
        print(f'streamkey: {key}')
        print('success')
    
@bot.command(name='meirl', help='Sends a meme from me_irl subreddit')
async def meirl(ctx):
    debug(ctx)
    print('contacting meme-api.herokuapp.com/gimme/me_irl')
    r = requests.get('https://meme-api.herokuapp.com/gimme/me_irl')
    rdata = json.loads(r.text)
    subreddit = rdata['subreddit']
    author = rdata['author']
    await ctx.send(f"I found this on `{subreddit}` from `{author}`: \n{rdata['url']}")
    print(rdata['url'])
    print('success')

@bot.command(name='wholesome', help='Sends you a wholesome meme')
async def wholesome(ctx):
    debug(ctx)
    print('contacting meme-api.herokuapp.com/gimme/wholesomememes')
    r = requests.get('https://meme-api.herokuapp.com/gimme/wholesomememes')
    rdata = json.loads(r.text)
    subreddit = rdata['subreddit']
    author = rdata['author']
    await ctx.send(f"I found this on `{subreddit}` from `{author}`: \n{rdata['url']}")
    print(rdata['url'])
    print('success')

@bot.command(name='dank', help='Sends you a dank-meme')
async def dank(ctx):
    debug(ctx)
    print('contacting meme-api.herokuapp.com/gimme/dankmemes')
    r = requests.get('https://meme-api.herokuapp.com/gimme/dankmemes')
    rdata = json.loads(r.text)
    subreddit = rdata['subreddit']
    author = rdata['author']
    await ctx.send(f"I found this on `{subreddit}` from `{author}`: \n{rdata['url']}")
    print(rdata['url'])
    print('success')

@bot.command(name='servers', help='Shows you how many servers the bot is connected to')
async def servers(ctx):
    debug(ctx)
    connectedServers = 0
    for i in bot.guilds:
        connectedServers += 1
    await ctx.send(f'currently connected to `{connectedServers}` servers!')

@bot.command(name='feedback', help='Sends you a link where you can give feedback to Maki!')
async def feedback(ctx):
    debug(ctx)
    await ctx.send('https://forms.gle/qydSqZad57PvGNL79 \nThank you! (´｡• ᵕ •｡`) ♡')

@bot.command(name='createuser', help='Creates a User in the Maki-Network! (wip)')
async def createUser(ctx):
    debug(ctx)
    #Check if the discord user id is already in the database
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT id FROM Users WHERE discord_id = {ctx.author.id}")
    mydb.commit()
    checkUser = mycursor.fetchall()
    if checkUser == []:
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(f"INSERT INTO Users (discord_id, balance, date_joined) VALUES ({ctx.author.id}, {100}, {time.time()})")
        mydb.commit()
        await ctx.send(f'Succesfully created a user for `{ctx.author.name}`. \nWelcome to the Maki-network! ＼(⌒▽⌒)')
    else:
        await ctx.send(f'User with your Discord-ID already exists in the database. ｡ﾟ･ (>﹏<) ･ﾟ｡')

@bot.command(name='userinfo', help='Gives you Information about your user on the Maki-database.')
async def userinfo(ctx):
    debug(ctx)
    try:
        balance = getBalance(ctx.author.id)
        timestamp = getCreationDate(ctx.author.id)
        userid = getUserID(ctx.author.id)
        await ctx.send(f'User: `{ctx.author.name}` \nUser-ID: `{userid}` \nDate created: `{timestamp}` \nBalance: `{balance} coins`')
    except:
        await ctx.send(f'Could not find user for `{ctx.author.name}` (×﹏×)\n->   try `+createuser`!')


@bot.command(name='balance', help='Shows you your balance in the Maki-database.')
async def balance(ctx):
    debug(ctx)
    try:
        await ctx.send(f'Your balance is `{getBalance(ctx.author.id)}` coins. ')
    except:
        await ctx.send(f'Could not find balance for `{ctx.author.name}` (×﹏×)\n->   try `+createuser`!')
    

@bot.event
async def on_command_error(ctx, error):
    debug(ctx)
    print(f"An error occured: {error}")
    await ctx.send(f"An error occured: `{str(error)}` (×﹏×)")


bot.run(TOKEN)
