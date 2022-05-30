from dependencies import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD')

intents = Intents.all()
client = Client(intents=intents)
tree = CommandTree(client)


@client.event
async def on_ready():
    print('Connected!')
    await tree.sync()


@tree.command(description='Responds with a random inspirational quote.')
async def inspiration(interaction: Interaction) -> None:
    request = requests.request('get', 'https://zenquotes.io?api=random')
    response = request.json()[0]
    quote = f":sparkles: *{response['q']}* :sparkles:"
    author = f"\u2014 {response['a']}"

    embed_msg = Embed(title=quote, colour=0xAEE1D3)
    embed_msg.set_footer(text=author)

    await interaction.response.send_message(embed=embed_msg)


@tree.command(description='Create a poll with up to 4 choices.')
async def poll(interaction: Interaction) -> None:
    await interaction.response.send_modal(Poll(client=client))


@tree.command(description='Create an event RSVP.')
async def rsvp(interaction: Interaction) -> None:
    await interaction.response.send_modal(Rsvp(client=client))

client.run(TOKEN)

