from dependencies import *


class RsvpButton(Button):
    def __init__(self, user, custom_id, label, emoji):
        super().__init__(custom_id=custom_id, label=label, emoji=emoji)
        self.user = user

    async def callback(self, interaction: Interaction):
        message_embed = interaction.message.embeds[0]

        new_embed = Embed(title=message_embed.title, colour=0xB8D0A6)
        new_embed.set_author(name=self.user.display_name + " created an event!", icon_url=self.user.avatar.url)

        for i, field in enumerate(message_embed.fields):
            new_value = field.value
            rsvp_list = field.value.split('\n')

            if self.custom_id == 'accept_button':
                new_value = self.edit_rsvp_list(interaction.user, rsvp_list, field.name, ':white_check_mark: Accepted')
            elif self.custom_id == 'decline_button':
                new_value = self.edit_rsvp_list(interaction.user, rsvp_list, field.name, ':x: Declined')
            elif self.custom_id == 'tentative_button':
                new_value = self.edit_rsvp_list(interaction.user, rsvp_list, field.name, ':grey_question: Tentative')

            new_embed.add_field(name=field.name, value=f"{new_value}", inline=field.inline)

        await interaction.response.edit_message(embed=new_embed)

        followup_message = f"Thanks for RSVP-ing to {self.user.display_name}'s event: __{message_embed.title}__ !"
        await interaction.followup.send(followup_message, ephemeral=True)

    def edit_rsvp_list(self, user, rsvp_list, field_name, field_name_check):
        if field_name == field_name_check:
            if "No one yet" in rsvp_list:
                rsvp_list.remove("No one yet")

            if user.display_name not in rsvp_list:
                rsvp_list.append(user.display_name)
        else:
            if user.display_name in rsvp_list:
                rsvp_list.remove(user.display_name)

                if not rsvp_list:
                    rsvp_list.append("No one yet")

        return "\n".join(rsvp_list)


class Rsvp(Modal, title='Create an RSVP Event'):
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

    def create_view(self, user):
        self.view = View(timeout=None)

        accept_button = RsvpButton(
            user=user,
            custom_id='accept_button',
            label='Going',
            emoji=PartialEmoji(name='✅')
        )

        decline_button = RsvpButton(
            user=user,
            custom_id='decline_button',
            label='Not Going',
            emoji=PartialEmoji(name='❌')
        )

        tentative_button = RsvpButton(
            user=user,
            custom_id='tentative_button',
            label='Maybe',
            emoji=PartialEmoji(name='❔')
        )

        self.view.add_item(accept_button)
        self.view.add_item(decline_button)
        self.view.add_item(tentative_button)

    def create_rsvp_embed_info(self, user, data):
        components = data['components']

        datetime_str = components[2]['components'][0]['value'] + " @ " + components[3]['components'][0]['value']

        self.embed.title = f":calendar_spiral: {components[0]['components'][0]['value']}"
        self.embed.add_field(name="Description", value=components[1]['components'][0]['value'], inline=False)
        self.embed.add_field(name="Date & Time", value=f'{datetime_str}', inline=False)
        self.embed.add_field(name="Location", value=components[4]['components'][0]['value'], inline=False)
        self.embed.add_field(name=":white_check_mark: Accepted", value="No one yet", inline=True)
        self.embed.add_field(name=":x: Declined", value="No one yet", inline=True)
        self.embed.add_field(name=":grey_question: Tentative", value="No one yet", inline=True)

        self.embed.set_author(name=user.display_name+" created an event!", icon_url=user.avatar.url)

        self.create_view(user)
