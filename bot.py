import os
import time
import utils
import requests

from dotenv import load_dotenv
from nextcord import Interaction, SlashOption, Intents
from nextcord.ext import commands

load_dotenv()

class Settings:
    def __init__(self):
        self._spam = False
        self._self_destruct = False
        self.intents = self._load_intents()       

    def _load_intents(self) -> Intents:
        intents = Intents.default()
        intents.presences = True
        intents.members = True
        intents.message_content = True
        return intents

    @property
    def spam(self):
        return self._spam

    @spam.setter
    def spam(self, value: bool):
        self._spam = value

    @property
    def self_destruct(self):
        return self._self_destruct

    @self_destruct.setter
    def self_destruct(self, value: bool):
        self._self_destruct = value

    @property
    def token(self):
        return os.getenv('BOT_TOKEN')


settings = Settings()

bot = commands.Bot(command_prefix="$", intents=settings.intents)

@bot.command()
async def ping(ctx):
    await ctx.send("hi")


@bot.command()
async def spam(ctx, count=5, *args):
    settings.spam = True
    for i in range(count):
        if settings.spam:
            for msg in args:
                await ctx.send(msg)
            time.sleep(0.2)


@bot.event
async def on_ready():
    print("ready")


@bot.listen()
async def on_message(message):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if str(message.author) == "Puma#0323":
        if str(message.content) == "kill on":
            settings.set_destruct = True
            await message.reply("Killmode activated")
        elif str(message.content) == "kill off":
            settings.set_destruct = False
            await message.reply("Killmode deactivated")
    elif (
        str(message.author) != "Puma#0323" and str(message.author) != "ChiefBacon#8835"
    ):
        requests.post(
            "https://maker.ifttt.com/trigger/msg_sent/with/key/cJ-Lon2D_aef5pPyH9-keR",
            json={
                "value1": f"{message.channel}",
                "value2": f"{message.author}: {message.content}",
                "value3": f"{message.author.avatar}",
            },
            headers=headers,
        )
        if settings.self_destruct:
            await message.delete()
    print(message.channel)
    print(f"{message.author}: {message.content}")


@bot.slash_command(
    name="regmlbb",
    description="Registers Your Discord id with your Mobile Legends Id",
)
async def register_mlbb(
        interaction: Interaction,
        uid: int = SlashOption(description="User ID", required=True),
        zid: int = SlashOption(description="Zone ID", required=True),
):
    db = utils.DataBase(interaction.guild_id)
    added_status = await db.add_to_mlbb_db(interaction.user.id, uid, zid)
    await interaction.response.send_message(added_status["message"])


"""@bot.slash_command(description="Fetches Apex Stats (WIP)")
async def apex_stats():
    pass"""

@bot.slash_command(description="Manages Minecraft Servers")
async def aternos(interaction: Interaction, action: str=SlashOption(description="ls|start|stop|v", required=True), server: str=SlashOption(description="server domain",required=False)):
    aternos = settings._aternos
    def ls():
        msg = ""
        for svr in aternos.list_servers():
            msg += f"{svr.domain}\t{svr.players_count}/{svr.slots}\n"
        return msg

    def v(svr):
        msg = ""
        msg += f"{svr.subdomain}\n"
        msg += f"{svr.motd}\n"
        msg += f"Server Status: {svr.status}\n"
        msg += f"Online: {svr.players_count} of {svr.slots}\n"
        return msg

    if action in ['ls', 'start', 'stop', 'v']:
        if not server:
            server = settings._main
        so = None
        for i in aternos.list_servers():
            if i.domain == server:
                so = i
        match action:
            case "ls":
                await interaction.response.send_message(ls())
            case 'start':
                so.start(headstart=True)
                await interaction.send(f"{so.domain} starting")
            case 'stop':
                so.stop()
                await interaction.response.send_message(f"{so.domain} stopping")
            case 'v':
                await interaction.send(v(so))


@bot.slash_command(description="Send your ideas to the Trello board")
async def idea(
    interaction: Interaction,
    idea: str = SlashOption(description="Your Idea", required=True),
):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    requests.post(
        "https://maker.ifttt.com/trigger/trello_idea/with/key/cJ-Lon2D_aef5pPyH9-keR",
        json={"value1": f"{idea}"},
        headers=headers,
    )
    await interaction.response.send_message("Done")


@bot.slash_command(description="Kills the spam")
async def spamkill(interaction: Interaction):
    settings.spam = False
    await interaction.response.send_message("Spam killed.")


if __name__ == "__main__":
    bot.run(settings.token)
