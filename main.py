import os
import requests
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")


@bot.command(name='inspo', help='Responds with a random inspirational quote')
async def inspirational_quote(ctx):
    request = requests.request('get', 'https://zenquotes.io?api=random')
    response = request.json()[0]
    quote = f":sparkles: *{response['q']}* :sparkles:"
    author = f"\u2014 {response['a']}"

    embed_msg = discord.Embed(title=quote, colour=0xAEE1D3)
    embed_msg.set_footer(text=author)

    await ctx.send(embed=embed_msg)


bot.run(TOKEN)
