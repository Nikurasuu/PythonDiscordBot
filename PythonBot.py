import os
import random

from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='+')
@bot.event
async def on_ready():

    print('connected (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

@bot.command(name='uwu', help='Respons with something even more cute', )
async def uwu(ctx):
    response = "UwU"
    await ctx.send(response)

@bot.command(name='age', help='Learn about this bot (*^^*)')
async def age(ctx):
    response = "Ich wurde am 19.01.2021 von @Niku#6103 erstellt! (´• ω •`)ﾉ "
    await ctx.send(response)

@bot.command(name='rolldice', help='Rolls a dice for you (+rolldice [amount] [sides])')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    for _ in range(number_of_dice):
        rolled_number = random.randint(1,number_of_sides)
        await ctx.send(f'rolled: {rolled_number}')

@bot.command(name='spam', help='spams for you (+spam [amount])')
async def spam(ctx, number_of_dice: int):
    for _ in range(number_of_dice):
        await ctx.send('OWO')

@bot.command(name='magic', help='Shows you some magic ✧')
async def magic(ctx):
    await ctx.send('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

@bot.command(name='japaneseemoji', help='Shows you a random japanese emoji (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
async def emoji(ctx):
    await ctx.send('still a work in progress. u-u')


bot.run(TOKEN)
