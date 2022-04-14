from dependencies import *


class Poll(Modal, title="Create a Poll"):
    name = TextInput(label="Title", placeholder="Poll Title", max_length=200)

    choice1 = TextInput(label="Choice 1", max_length=200)
    choice2 = TextInput(label="Choice 2", max_length=200)
    choice3 = TextInput(label="Choice 3", max_length=200, required=False)
    choice4 = TextInput(label="Choice 4", max_length=200, required=False)

    async def on_submit(self, interaction: Interaction) -> None:
        print(interaction.data)
        await interaction.response.send_message('Poll created!', ephemeral=True)

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_tb(error.__traceback__)
