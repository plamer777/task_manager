"""This file contains a Command class to execute a custom command"""
import os
from django.core.management import BaseCommand
from bot.tg.client import TgClient
from bot.tg.bot_actions import BotActions

# -------------------------------------------------------------------------

token = os.environ.get("TG_TOKEN")
bot_actions = BotActions()
client = TgClient(token, bot_actions)


class Command(BaseCommand):
    """Command class representing a custom command to run a telegram bot"""

    help = "Starts a telegram bot"

    def handle(self, *args, **options) -> None:
        """This method starts a telegram bot"""
        client.start_bot()
