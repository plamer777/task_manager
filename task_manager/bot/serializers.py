"""This file contains serializer classes for telegram bot models"""
from rest_framework import serializers
from bot.models import TgUser

# -------------------------------------------------------------------------


class BotUpdateSerializer(serializers.ModelSerializer):
    """This serializer used to serialize and deserialize TgUser model"""

    class Meta:
        model = TgUser
        fields = "__all__"
        read_only_fields = ["tg_id", "username", "user"]
