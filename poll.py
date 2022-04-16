from dependencies import *


class PollButton(Button):
    async def callback(self, interaction):
        await interaction.response.edit_message(content='button clicked', view=None)


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
        print(interaction.data)

        def check(x):
            print(x)
            return True

        # while True:
        res = await self.client.wait_for(
            'button_click',
            check=check
        )

        await interaction.response.send_message("button clicked", ephemeral=True)
#     print(res)

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

    def create_poll_embed_info(self, user, data):
        poll_info = {}
        poll_body = ""

        choice_num = 1

        self.view = View()

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
                        poll_body += f":{self.numbers_emojis[choice_num]}: {value}\n"
                        button = PollButton(custom_id=custom_id, label=f"{choice_num}")
                        self.view.add_item(item=button)
                        choice_num += 1

        self.embed.title = poll_title
        self.embed.set_author(name=user.display_name+" created a poll!", icon_url=user.avatar.url)
        self.embed.add_field(name="Vote from these choices:", value=poll_body)

        return {'number_emojis': self.numbers_emojis, 'poll_info': poll_info, 'num_choices': choice_num}