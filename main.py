import os

import discord
import requests

from dotenv import load_dotenv
from discord import Embed, Intents, Interaction, Client
from discord.ext import commands
from discord.ui import Modal
from discord.app_commands import CommandTree

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD')

intents = Intents.all()
client = Client(intents=intents)
tree = CommandTree(client)

test_guild = discord.Object(id=GUILD)


@client.event
async def on_ready():
    print('Connected!')
    await tree.sync(guild=test_guild)


@tree.command(guild=test_guild, description='Responds with a random inspirational quote.')
async def inspiration(interaction):
    request = requests.request('get', 'https://zenquotes.io?api=random')
    response = request.json()[0]
    quote = f":sparkles: *{response['q']}* :sparkles:"
    author = f"\u2014 {response['a']}"

    embed_msg = Embed(title=quote, colour=0xAEE1D3)
    embed_msg.set_footer(text=author)

    await interaction.response.send_message(embed=embed_msg)


# @tree.command(guild=test_guild, description="Create a poll with up to 5 choices.")
# async def poll(interaction: Interaction):
#     poll_modal = Modal(title="Create a Modal")
#     await interaction.response.send_modal(poll_modal)


client.run(TOKEN)

