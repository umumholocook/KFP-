from common.KfpDbUtil import KfpDbUtil
import discord
import os
import tempfile
from pathlib import Path
from subprocess import Popen
from discord.ext import commands
from common.KFP_DB import KfpDb

VERSION = "0.0.1"
TOKEN=os.environ['KFP_TOKEN']
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '!',intents = intents)

def getTempFile():
    return Path('{}/kpf_restart'.format(tempfile.gettempdir()))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(' --  --  -- ')

    tmpFile = getTempFile()
    if tmpFile.exists():
        os.remove(tmpFile.absolute())
        db = KfpDb()
        channel_id = db.get_reboot_message_channel()
        if channel_id:
            await bot.get_channel(channel_id).send("更新完成")

@bot.event
async def on_message(message):
    print('on_message get message from {0.author} : {0.content}'.format(message)) if message.author.id != bot.user.id else None
    ctx = await bot.get_context(message)
    if ctx.command != None:
        await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    print('on_command_completion Command {0.name} completion'.format(ctx.command))
    #await ctx.message.delete()

@bot.command(name = 'invite_link',invoke_without_command = True)
async def command_invite_link(ctx, *attr):
    link = "https://discordapp.com/oauth2/authorize?&client_id={}&scope=bot&permissions={}".format(bot.user.id, 1543892049)
    await ctx.send(link)

@bot.command(name = 'update',invoke_without_command = True)
async def command_restart(ctx, *attr):
    db = KfpDb()
    db.set_reboot_message_channel(channel_id=ctx.channel.id)
    await ctx.send("重新啟動中...")
    getTempFile().touch()
    bot.loop.stop()
    Popen(['update_and_restart.sh'], shell=True)

@bot.command(name = 'version',invoke_without_command = True)
async def command_get_version(ctx, *attr):
    await ctx.send(VERSION)

@bot.command(name = 'import_data', invoke_without_command = True)
async def import_data(ctx, *attr):
    await ctx.send("導入舊有資料中...")
    newCount = KfpDbUtil.importFromOldDatabase(ctx.guild.id, "KFP_bot_old.db")
    oldCount = KfpDbUtil.getCount(ctx.guild.id, "KFP_bot_old.db") 
    await ctx.send("導入結束資料中... 舊有資料{}筆, 導入{}筆".format(oldCount, newCount))

@bot.group(name = 'cogs', invoke_without_command = True)
async def cogs_group(ctx, *attr):
    description = 'cogs:\n'
    for file in os.listdir(r'./cogs'):
        if file.endswith('.py'):
            description += '  |- {}\n'.format(file[:-3])
    await ctx.send(description)

@cogs_group.command(name = 'load')
@commands.is_owner()
async def cogs_load(ctx, extention):
    bot.load_extension(f'cogs.{extention}')

@cogs_group.command(name = 'unload')
@commands.is_owner()
async def cogs_unload(ctx, extention):
    bot.unload_extension(f'cogs.{extention}')

@cogs_group.command(name = 'reload')
@commands.is_owner()
async def cogs_reload(ctx, extention):
    bot.unload_extension(f'cogs.{extention}')
    bot.load_extension(f'cogs.{extention}')
    ctx.send('reload cog {}'.format(extention))

#preload cogs
temp = 'load cogs:\n'
for file in os.listdir(r'./cogs'):
    if not file.endswith('_test.py') and not file.startswith("__init__") and file.endswith('.py'):
        temp += '  |- {}\n'.format(file[:-3])
        bot.load_extension('cogs.{}'.format(file[:-3]))
print(temp)

bot.run(TOKEN)
