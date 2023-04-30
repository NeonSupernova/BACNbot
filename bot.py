import time
import DataBase
import MLBBApi
import ApexApi
import requests

from nextcord import Interaction, SlashOption, Intents
from nextcord.ext import commands


my_intents = Intents.default()
my_intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=my_intents)
openai.api_key = "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"


class Settings:
    def __init__(self):
        self.spam = False
        self.self_destruct = False

    def set_spam(self, value: bool):
        self.spam = value

    def set_destruct(self, value: bool):
        self.self_destruct = value


settings = Settings()


@bot.command()
async def ping(ctx):
    await ctx.send("hi")


@bot.command()
async def spam(ctx, count=5, *args):
    settings.set_spam(True)
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
            settings.set_destruct(True)
            await message.reply("Killmode activated")
        elif str(message.content) == "kill off":
            settings.set_destruct(False)
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
    name="register mlbb",
    description="Registers Your Discord id with your Mobile Legends Id",
)
async def register_mlbb(
    interaction: Interaction,
    uid: int = SlashOption(description="User ID", required=True),
    zid: int = SlashOption(description="Zone ID", required=True),
):
    db = DataBase.DataBase(interaction.guild_id)
    added_status = await db.add_to_mlbb_db(interaction.user.id, uid, zid)
    await interaction.response.send_message(added_status["message"])


@bot.slash_command(description="Fetches Apex Stats (WIP)")
async def apex_stats():
    pass


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
async def spam_kill(interaction: Interaction):
    settings.set_spam(False)
    await interaction.response.send_message("Spam killed.")


if __name__ == "__main__":
    bot.run("OTk2NTUzMjkwNzg1NDk3MTc5.G_wtgP.VBniNkoi--JA_h8iNla18yMB9E0lp_2QcFmDbk")
