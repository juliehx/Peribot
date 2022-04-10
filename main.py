# # # # # # # # # # # # # #
#         PERIBOT         #
# # # # # # # # # # # # # #

import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:
        print(f'Member of {guild.name} (id:{guild.id})')
        print('Members:')
        for member in guild.members:
            print(f'{member.name}')


client.run(TOKEN)
