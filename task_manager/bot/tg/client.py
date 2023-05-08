"""This file contains a TgClient class to manage telegram bot"""
import logging
from string import ascii_lowercase, digits
from random import choice
import requests
from django.db import transaction
from marshmallow import ValidationError
from marshmallow_dataclass import class_schema
from requests import Response
from bot.models import TgUser
from bot.tg.bot_actions import BotActions
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, Update
from django.conf import settings
# -------------------------------------------------------------------------

logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO)


class TgClient:
    """TgClient class contains methods to manage telegram bot"""

    def __init__(
            self, bot_actions: BotActions,
            token: str = settings.TG_TOKEN) -> None:
        """Initialize the TgClient class
        :param token: A string representing the telegram bot token
        :param bot_actions: A BotActions instance
        """
        self._token = token
        self._all_actions = bot_actions
        self._state_actions = {
            TgUser.BotStates.remove_goal: self._all_actions.remove_goal,
            TgUser.BotStates.wait_category: self._all_actions.set_category,
            TgUser.BotStates.wait_title: self._all_actions.create_goal,
        }
        self._command_actions = {
            '/goals': self._all_actions.get_user_goals,
            '/create': self._all_actions.get_user_categories,
            '/remove': self._all_actions.get_removable_goals,
        }

    def get_url(self, method: str) -> str:
        """This method returns the configured telegram url
        :param method: A string representing a method to add in telegram url
        :return: A string representing the telegram url with token and
        requested method
        """
        return f"https://api.telegram.org/bot{self._token}/{method}"

    def get_updates(
            self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """This method serves to send update request to telegram API,
        get response and return GetUpdatesResponse instance
        :param offset: An integer representing the offset to get certain
        update message
        :param timeout: An integer representing the seconds to wait for
        response
        :return: A GetUpdatesResponse instance
        """
        response = self._get_response(
            'getUpdates', offset=offset, timeout=timeout)

        updates_response_schema = class_schema(GetUpdatesResponse)()
        try:
            return updates_response_schema.load(response.json())
        except ValidationError as e:
            logging.exception(f'There was an error during update: {e}')
            return GetUpdatesResponse(ok=False, result=[])

    def send_message(self, chat_id: int, message: str) -> SendMessageResponse:
        """This method serves to send a message to telegram API
        :param chat_id: An integer representing the telegram chat id
        :param message: A string representing the message to send
        :return: A SendMessageResponse instance containing a result of the
        operation
        """
        response = self._get_response(
            'sendMessage', chat_id=chat_id, text=message)

        message_response_schema = class_schema(SendMessageResponse)()
        try:
            return message_response_schema.load(response.json())
        except ValidationError as e:
            logging.exception(
                f'There was an error during sending message: {e}')
        return SendMessageResponse(ok=False, message=None)

    def _get_response(self, method: str, **params) -> Response:
        """This additional method serves to get a response from telegram by
        provided method and parameters
        :param method: A string representing the telegram method
        :param params: Key-value pairs of parameters
        """
        url = self.get_url(method)
        response = requests.get(url, params=params)
        if not response.ok:
            raise ValueError('Status is not ok')

        return response

    def start_bot(self) -> None:
        """This is a main method to start the telegram bot"""
        offset = 0
        while True:
            try:
                response = self.get_updates(offset=offset)
                new_code = self._generate_code()

                for item in response.result:
                    offset = item.update_id + 1
                    logging.info(
                        f'Message received from telegram {item.message}')
                    tg_user, is_created = self._get_or_create_tg_user(
                        item, new_code)

                    if is_created:
                        message = (
                            f"Привет {item.message.from_.first_name}.\n"
                            f"Ваш код верификации: {new_code}"
                        )

                    elif tg_user.bot_state == TgUser.BotStates.added:
                        message = self._all_actions.confirm_user(
                            item, new_code)

                    elif tg_user.bot_state == TgUser.BotStates.confirmed:
                        message = self._get_confirmed_user_options(
                            item, tg_user)

                    else:
                        message = self._get_state_options(item, tg_user)

                    message_response = self.send_message(
                        item.message.chat.id, message)
                    logging.info(f'Message response: {message_response}')

            except Exception as e:
                logging.exception(f'There was an error: {e}')

    @staticmethod
    def _generate_code() -> str:
        """This secondary method serves to generate a random code to verify
        user
        :return: A string representing generated code
        """
        code_length = 15
        symbols = ascii_lowercase + digits
        new_code = [choice(symbols) for _ in range(code_length)]
        return "".join(new_code)

    @staticmethod
    def _get_or_create_tg_user(
            item: Update, new_code: str) -> tuple[TgUser, bool]:
        """This method creates a new telegram user or returns existing one
        :param item: An instance of Update class
        :param new_code: A string representing a random code
        """
        with transaction.atomic():
            tg_user, is_created = TgUser.objects.get_or_create(
                tg_id=item.message.chat.id,
                username=item.message.from_.username,
            )
            if is_created:
                tg_user.verification_code = new_code
                tg_user.save()

        return tg_user, is_created

    def _get_confirmed_user_options(self, item: Update, tg_user: TgUser) -> str:
        """This method used to provide options for confirmed users
        :param item: An instance of Update class
        :param tg_user: An instance of TgUser class
        :return: A string representing the message to send to telegram bot
        """
        action = self._command_actions.get(item.message.text)

        if not action:
            message = "Неизвестная команда"
        else:
            message = action(tg_user)

        return message

    def _get_state_options(self, item: Update, tg_user: TgUser) -> str:
        """This method used to provide options for current state of
        telegram bot
        :param item: An instance of Update class
        :param tg_user: An instance of TgUser class
        :return: A string representing the message to send to telegram bot
        """
        if item.message.text == "/cancel":
            message = self._all_actions.cancel_request(tg_user)
        else:
            action = self._state_actions.get(tg_user.bot_state)
            if not action:
                return "Неизвестный запрос"

            message = action(item.message.text, tg_user)

        return message
