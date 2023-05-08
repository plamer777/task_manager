"""This file contains CBVs for telegram bot"""
from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from bot.tg import client
from bot.models import TgUser
from bot.serializers import BotUpdateSerializer

# --------------------------------------------------------------------------


class BotConfirmView(generics.UpdateAPIView):
    """This view used to connect telegram user with application user"""

    serializer_class = BotUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "verification_code"

    def get_queryset(self):
        self.kwargs["verification_code"] = self.request.data.get(
            "verification_code")
        queryset = TgUser.objects.filter(
            verification_code=self.kwargs["verification_code"]
        )
        if not queryset:
            raise ValidationError({"verification_code": "incorrect"}, code=400)
        return queryset

    def perform_update(self, serializer: BotUpdateSerializer) -> None:
        """This method used to connect telegram user with application user
        and change bot_state"""
        with transaction.atomic():
            tg_user = serializer.save()
            tg_user.user = self.request.user
            tg_user.bot_state = TgUser.BotStates.confirmed
            tg_user.save()

        client.send_message(tg_user.tg_id, "Аккаунт успешно подтвержден")
