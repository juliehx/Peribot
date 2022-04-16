import os
import traceback

import discord
import requests

from dotenv import load_dotenv

from discord.app_commands import CommandTree
from discord.ui import (
    Modal,
    TextInput,
    Button,
    View,
)
from discord import (
    Embed,
    Intents,
    Interaction,
    Client,
    Emoji,
    PartialEmoji
)

from poll import Poll
