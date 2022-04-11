import os
import requests

from dotenv import load_dotenv
from discord import Embed, Intents
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print('Connected!')


@bot.command(help="Responds with a random inspirational quote")
async def inspiration(ctx):
    request = requests.request('get', 'https://zenquotes.io?api=random')
    response = request.json()[0]
    quote = f":sparkles: *{response['q']}* :sparkles:"
    author = f"\u2014 {response['a']}"

    embed_msg = Embed(title=quote, colour=0xAEE1D3)
    embed_msg.set_footer(text=author)

    await ctx.send(embed=embed_msg)


# @bot.command(name='poll', help='Create a poll')
# async def poll(ctx):
#     await ctx.interactions.send_message()


bot.run(TOKEN)
