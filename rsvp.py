from dependencies import *


class Rsvp(Modal, title='Create and RSVP'):
    event_name = TextInput(custom_id="event_name", label="Event", placeholder="Event Name", max_length=200)
    description = TextInput(custom_id="event_description", label="Description", max_length=500)
    date = TextInput(custom_id="event_date", label="Date")
    time = TextInput(custom_id="event_time", label="Time")
    location = TextInput(custom_id="event_address", label="Location")

    def __init__(self, client: Client):
        super().__init__()

        self.client = client
        self.on_submit = self.client.event(self.on_submit)
        self.view = None
        self.embed = Embed(colour=0xB8D0A6)

    async def on_submit(self, interaction: Interaction) -> None:
        self.create_rsvp_embed_info(interaction.user, interaction.data)
        await interaction.response.send_message(embed=self.embed, view=self.view)

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

    def create_rsvp_embed_info(self, user, data):
        components = data['components']

        datetime_str = components[2]['components'][0]['value'] + " @ " + components[3]['components'][0]['value']

        self.embed.title = f":calendar_spiral: {components[0]['components'][0]['value']}"
        self.embed.add_field(name="Description", value=components[1]['components'][0]['value'], inline=False)
        self.embed.add_field(name="Date & Time", value=f'{datetime_str}', inline=False)
        self.embed.add_field(name=":white_check_mark: Accepted", value="No one yet", inline=True)
        self.embed.add_field(name=":x: Declined", value="No one yet", inline=True)
        self.embed.add_field(name=":grey_question: Tentative", value="No one yet", inline=True)

        self.embed.set_author(name=user.display_name+" created an event!", icon_url=user.avatar.url)

