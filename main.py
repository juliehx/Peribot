from dependencies import *

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
    tree.remove_command("inspiration")
    tree.remove_command("poll")
    await tree.sync(guild=test_guild)


@tree.command(guild=test_guild, description='Responds with a random inspirational quote.')
async def inspiration(interaction: Interaction) -> None:
    request = requests.request('get', 'https://zenquotes.io?api=random')
    response = request.json()[0]
    quote = f":sparkles: *{response['q']}* :sparkles:"
    author = f"\u2014 {response['a']}"

    embed_msg = Embed(title=quote, colour=0xAEE1D3)
    embed_msg.set_footer(text=author)

    await interaction.response.send_message(embed=embed_msg)


@tree.command(guild=test_guild, description='Create a poll with up to 4 choices.')
async def poll(interaction: Interaction) -> None:
    await interaction.response.send_modal(Poll(client=client))


client.run(TOKEN)

