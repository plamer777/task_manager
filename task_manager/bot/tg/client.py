"""This file contains a TgClient class to manage telegram bot"""
from string import ascii_lowercase, digits
from random import choice
import requests
from marshmallow_dataclass import class_schema
from bot.models import TgUser
from bot.tg.bot_actions import BotActions
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, Update

# -------------------------------------------------------------------------


class TgClient:
    """TgClient class contains methods to manage telegram bot"""
    def __init__(self, token: str, bot_actions: BotActions) -> None:
        """Initialize the TgClient class
        :param token: A string representing the telegram bot token
        :param bot_actions: A BotActions instance
        """
        self._token = token
        self._bot_actions = bot_actions
        self._actions = {
            TgUser.BotStates.remove_goal: self._bot_actions.remove_goal,
            TgUser.BotStates.wait_category: self._bot_actions.set_category,
            TgUser.BotStates.wait_title: self._bot_actions.create_goal
        }

    def get_url(self, method: str) -> str:
        """This method returns the configured telegram url
        :param method: A string representing a method to add in telegram url
        :return: A string representing the telegram url with token and
        requested method
        """
        return f'https://api.telegram.org/bot{self._token}/{method}'

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
        url = self.get_url('getUpdates')
        updates_url = f'{url}?offset={offset}&timeout={timeout}'
        response = requests.get(updates_url)

        if not response:
            raise NotImplementedError

        updates_response_schema = class_schema(GetUpdatesResponse)()
        result = updates_response_schema.load(response.json())

        return result

    def send_message(self, chat_id: int, message: str) -> SendMessageResponse:
        """This method serves to send a message to telegram API
        :param chat_id: An integer representing the telegram chat id
        :param message: A string representing the message to send
        :return: A SendMessageResponse instance containing a result of the
        operation
        """
        url = self.get_url('sendMessage')
        message_url = f'{url}?chat_id={chat_id}&text={message}'
        response = requests.get(message_url)

        if not response:
            raise NotImplementedError

        message_response_schema = class_schema(SendMessageResponse)()
        result = message_response_schema.load(response.json())
        return result

    def start_bot(self) -> None:
        """This is a main method to start the telegram bot"""
        offset = 0

        while True:
            response = self.get_updates(offset=offset)
            new_code = self._generate_code()
            for item in response.result:
                offset = item.update_id + 1
                print(item.message)

                username = item.message.from_.username
                tg_user_queryset = TgUser.objects.filter(username=username)
                tg_user = tg_user_queryset.first()

                if not tg_user_queryset.exists():

                    message = (f'Привет {item.message.from_.first_name}.\n'
                               f'Ваш код верификации: {new_code}')
                    self._create_tg_user(item, new_code)

                elif tg_user.bot_state == TgUser.BotStates.added:
                    message = self._bot_actions.confirm_user(item, new_code)

                elif tg_user.bot_state == TgUser.BotStates.confirmed:

                    message = self._get_confirmed_user_options(item, tg_user)

                else:
                    message = self._get_state_options(item, tg_user)

                message_response = self.send_message(
                    item.message.chat.id, message)
                print(message_response)

    @staticmethod
    def _generate_code() -> str:
        """This secondary method serves to generate a random code to verify
        user
        :return: A string representing generated code
        """
        code_length = 15
        symbols = ascii_lowercase + digits
        new_code = [choice(symbols) for _ in range(code_length)]
        return ''.join(new_code)

    @staticmethod
    def _create_tg_user(item: Update, new_code: str) -> None:
        """This method creates a new telegram user
        :param item: An instance of Update class
        :param new_code: A string representing a random code
        """
        TgUser.objects.create(
            tg_id=item.message.chat.id,
            username=item.message.from_.username,
            verification_code=new_code,
            bot_state=TgUser.BotStates.added
        )

    def _get_confirmed_user_options(self, item: Update, tg_user: TgUser) -> str:
        """This method used to provide options for confirmed users
        :param item: An instance of Update class
        :param tg_user: An instance of TgUser class
        :return: A string representing the message to send to telegram bot
        """
        if item.message.text == '/goals':
            message = self._bot_actions.get_user_goals(
                tg_user
            )
        elif item.message.text == '/create':
            message = self._bot_actions.get_user_categories(
                tg_user
            )

        elif item.message.text == '/remove':
            message = 'Введите имя цели:\n' + self._bot_actions.get_user_goals(
                tg_user
            )
            tg_user.bot_state = TgUser.BotStates.remove_goal
            tg_user.save()

        else:
            message = 'Неизвестная команда'

        return message

    def _get_state_options(self, item: Update, tg_user: TgUser) -> str:
        """This method used to provide options for current state of
        telegram bot
        :param item: An instance of Update class
        :param tg_user: An instance of TgUser class
        :return: A string representing the message to send to telegram bot
        """
        if item.message.text == '/cancel':
            message = self._bot_actions.cancel_request(
                tg_user
            )
        else:
            action = self._actions.get(tg_user.bot_state)
            if not action:
                return 'Неизвестный запрос'

            message = action(
                item.message.text,
                tg_user,
            )

        return message
