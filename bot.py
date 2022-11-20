import nextcord
from nextcord import Interaction, SlashOption, Intents
from nextcord.ext import commands
import aiomlbb
import sqlite3
import os
import requests
import time
import asyncio
import sys


async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
        None, lambda s=string: sys.stdout.write(s + ' '))
    return await asyncio.get_event_loop().run_in_executor(
        None, sys.stdin.readline)


async def console(ctx, channel=None):
    x = await ainput(f"{channel}>> ")
    if x == "set":
        n == 0
        for i in ctx.guild.channels:
            print(f"{n} {i}")
        num = await ainput(">> ")
        channel = ctx.guild.channels[num]
    return x, channel


async def add_to_db(discord_name, discord_id, user_id, zone_id):
    cli = aiomlbb.MLBBApi(user_id, zone_id)
    data = await cli.get('username')
    if data['status'] == 'success':
        con = sqlite3.connect('registry.db')
        cur = con.cursor()
        CREDS = (discord_name, discord_id, int(user_id), int(zone_id))
        for row in cur.execute('SELECT * FROM Registry'):
            if row == CREDS:
                return {'status': False, 'message': 'Already Registered'}
        cur.execute('INSERT INTO Registry VALUES (?, ?, ?, ?)', CREDS)
        con.commit()
        con.close()
        return {'status': True, 'message': 'Registered Successfully'}
    else:
        return {'status': False, 'message': 'Invalid Login Credentials'}


my_intents = Intents.default()
my_intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=my_intents)


@bot.command()
async def ping(ctx):
    await ctx.send('hi')


@bot.command()
async def play(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    playlist = os.listdir('Music')
    playlist.sort()
    music = []
    for i in playlist:
        source = nextcord.FFmpegOpusAudio("Music/" + i)
        music.append(source)
    if ctx.voice_client.is_connected():
        await ctx.voice_client.play(source)
        await ctx.send(f'Playing in {ctx.voice_client.channel}')
    else:
        ctx.send('Not Connected')


@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        return await ctx.voice_client.disconnect()
    else:
        await ctx.send("Not In a channel")


@bot.command()
async def pingofdeath(ctx, count=5, *args):
    for i in range(count):
        for victim in args:
            await ctx.send(victim)
        time.sleep(0.2)


@bot.event
async def on_ready():
    print('ready')


@bot.listen()
async def on_message(message):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    if str(message.author) != "Puma#0323":
        requests.post("https://maker.ifttt.com/trigger/msg_sent/with/key/cJ-Lon2D_aef5pPyH9-keR",
                      json={"value1": f"{message.channel}", "value2": f"{message.author}: {message.content}",
                            "value3": f"{message.author.avatar}"}, headers=headers)

    print(message.channel)
    print(f"{message.author}: {message.content}")


@bot.slash_command(description="Registers Your Discord id with your Mobile Legends Id")
async def register(
        interaction: Interaction,
        uid: str = SlashOption(description="User ID", required=True),
        zid: str = SlashOption(description="Zone ID", required=True)
):
    added_status = await add_to_db(interaction.user.name, interaction.user.id, uid, zid)
    await interaction.response.send_message(added_status['message'])


@bot.slash_command(description="Send your ideas to the Trello board")
async def idea(
        interaction: Interaction,
        idea: str = SlashOption(description="Your Idea", required=True)):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    requests.post("https://maker.ifttt.com/trigger/trello_idea/with/key/cJ-Lon2D_aef5pPyH9-keR",
                  json={"value1": f"{idea}"}, headers=headers)
    await interaction.response.send_message("Done")


bot.run('OTk2NTUzMjkwNzg1NDk3MTc5.G_wtgP.VBniNkoi--JA_h8iNla18yMB9E0lp_2QcFmDbk')
