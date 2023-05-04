"""This file contains TgUser model to create and get telegram user records"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User

# -------------------------------------------------------------------------


class TgUser(models.Model):
    """TgUser model with necessary attributes"""

    class BotStates(models.IntegerChoices):
        """This class provides states available for bot_state field"""

        added = 1, _("Added")
        confirmed = 2, _("Confirmed")
        wait_category = 3, _("Wait Category")
        wait_title = 4, _("Wait Title")
        remove_goal = 5, _("Remove Goal")

    tg_id = models.IntegerField(verbose_name=_("Telegram chat"))
    username = models.CharField(verbose_name=_("Telegram user"), max_length=50)
    bot_state = models.PositiveSmallIntegerField(
        choices=BotStates.choices, verbose_name=_("Bot State"), default=BotStates.added
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    verification_code = models.CharField(
        verbose_name=_("Verification code"), null=True, max_length=15
    )

    class Meta:
        verbose_name = _("Telegram user")
        verbose_name_plural = _("Telegram users")

    def __str__(self):
        return self.username
