"""This file contains a Command class to execute a custom command"""
from django.core.management import BaseCommand
from bot.tg import client

# -------------------------------------------------------------------------


class Command(BaseCommand):
    """Command class representing a custom command to run a telegram bot"""

    help = "Starts a telegram bot"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the Command class"""
        super().__init__(*args, **kwargs)
        self.client = client

    def handle(self, *args, **options) -> None:
        """This method starts a telegram bot"""
        self.client.start_bot()
