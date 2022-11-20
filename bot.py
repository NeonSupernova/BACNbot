import nextcord
from nextcord import Interaction, SlashOption, Intents
from nextcord.ext import commands
import aiomlbb
import sqlite3
import os


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
async def test(ctx):
    await ctx.send('hi')


@commands.command()
async def join(ctx, *, channel: nextcord.VoiceChannel):
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()

bot.add_command(join)


@bot.command()
async def play(ctx):
    playlist = os.listdir('Music')
    playlist.sort()
    source = nextcord.FFmpegOpusAudio(f'./Music/{playlist[2]}')
    ctx.voice_client.play(source)
    await ctx.send(f'Playing in {ctx.voice_client}')


@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        return await ctx.voice_client.disconnect()
    else:
        await ctx.send("Not In a channel")
import time
@bot.command()
async def onethousandpingsofdeath(ctx):
    for i in range(1000):
        await ctx.send("@ArdentMedusa")
        time.sleep(0.1)

@bot.slash_command(description="Registers Your Discord id with your Mobile Legends Id")
async def register(
        interaction: Interaction,
        uid: str = SlashOption(description="User ID", required=True),
        zid: str = SlashOption(description="Zone ID", required=True)
):
    added_status = await add_to_db(interaction.user.name, interaction.user.id, uid, zid)
    await interaction.response.send_message(added_status['message'])

bot.run('OTk2NTUzMjkwNzg1NDk3MTc5.G_wtgP.VBniNkoi--JA_h8iNla18yMB9E0lp_2QcFmDbk')
