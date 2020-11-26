from functools import wraps

import discord
from discord.ext import commands

from config import settings
from txts import *

global commands_dict

ver = '0.0.6'
commands_dict = {}

bot = commands.Bot (command_prefix = settings ['prefix'])

def add_command (name): #Не трогать: убью
    def adder (func):
        commands_dict [name] = func

        return func
    return adder
        
@bot.event #Не трогать: убью
async def on_ready ():
    print (ver)

    game = discord.Game (txt_status_before + ver + txt_status_after)
    await bot.change_presence (
        status = discord.Status.idle, 
        activity = game
    )

@add_command ('help') #Пример как делать комманды
async def help (message):
    await message.channel.send (embed = help_embed)
 


@bot.event #Не трогать: убью
async def on_message (message):
    if message.author.bot:
        return

    if message.content == 'help':
        await message.channel.send (
            txt_help_not_command_before + settings ['prefix'] + txt_help_not_command_after
        )

    check = lambda val: message.content.startswith (settings ["prefix"] + val)

    if check (''):
        for command_name in commands_dict:
            if check (command_name):
                await commands_dict [command_name] (message)

                break

        else:
            await message.channel.send (txt_no_command)

bot.run (settings ['token'])
