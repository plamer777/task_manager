from bot.tg.bot_actions import BotActions
from bot.tg.client import TgClient
# ------------------------------------------------------------------------
client = TgClient(BotActions())

__all__ = ['client']
