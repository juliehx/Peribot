from dependencies import *


class PollButton(Button):
    def __init__(self, user, custom_id, label):
        super().__init__(custom_id=custom_id, label=label)
        self.user = user

    async def callback(self, interaction):
        message_embed = interaction.message.embeds[0]

        new_embed = Embed(title=message_embed.title, colour=0xffe6a1)
        new_embed.set_author(name=self.user.display_name+" is hosting a poll!", icon_url=self.user.avatar.url)
        new_embed.add_field(name="Vote from these choices:", value="\u2014", inline=False)

        for i, field in enumerate(message_embed.fields[1:]):
            num_votes = int(field.value.split(' ')[0])
            if self.label == str(i+1):
                num_votes += 1

            new_embed.add_field(name=field.name, value=f"{num_votes} votes", inline=False)

        await interaction.response.edit_message(embed=new_embed)

        followup_message = f"Thanks for voting in {self.user.display_name}'s poll: __{message_embed.title}__ !"
        await interaction.followup.send(followup_message, ephemeral=True)


class Poll(Modal, title="Create a Poll"):
    name = TextInput(custom_id="poll_title", label="Title", placeholder="Poll Title", max_length=200)

    choice1 = TextInput(custom_id="poll_choice1", label="Choice 1", max_length=200)
    choice2 = TextInput(custom_id="poll_choice2", label="Choice 2", max_length=200)
    choice3 = TextInput(custom_id="poll_choice3", label="Choice 3", max_length=200, required=False)
    choice4 = TextInput(custom_id="poll_choice4", label="Choice 4", max_length=200, required=False)

    def __init__(self, client: Client):
        super().__init__()

        self.client = client
        self.on_submit = self.client.event(self.on_submit)
        self.view = None
        self.embed = Embed(colour=0xffe6a1)

        self.numbers_emojis = {1: "one", 2: "two", 3: "three", 4: "four"}

    async def on_submit(self, interaction: Interaction) -> None:
        self.create_poll_embed_info(interaction.user, interaction.data)
        await interaction.response.send_message(embed=self.embed, view=self.view)

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

    def create_poll_embed_info(self, user, data) -> None:
        poll_info = {}
        poll_body = ""

        choice_num = 1

        # todo: define separate view or include timeout in bot help command
        self.view = View(timeout=86400)
        self.embed.add_field(name="Vote from these choices:", value="\u2014", inline=False)

        poll_title = ":bar_chart: "
        for component in data['components']:
            custom_id = component['components'][0]['custom_id']
            value = component['components'][0]['value']

            if custom_id == "poll_title":
                poll_title += f"{value}"
            else:
                if value != '':
                    poll_info[custom_id] = 0

                    if custom_id != "poll_title":
                        field_name = f":{self.numbers_emojis[choice_num]}: {value}"
                        self.embed.add_field(name=field_name, value="0 votes", inline=False)

                        button = PollButton(user=user, custom_id=custom_id, label=f"{choice_num}")
                        self.view.add_item(item=button)

                        choice_num += 1

        self.embed.title = poll_title
        self.embed.set_author(name=user.display_name+" is hosting a poll!", icon_url=user.avatar.url)