"""This file contains classes to configure admin panel"""
from django.contrib import admin
from bot.models import TgUser

# -------------------------------------------------------------------------


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    """This class provides configuration for the telegram user section of the
    admin panel"""

    list_display = ("username", "bot_state", "user")
    search_fields = ("username", "user")
    readonly_fields = ("username", "tg_id")
