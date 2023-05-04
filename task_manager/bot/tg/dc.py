"""This file contains dataclasses representing different parts of telegram API
response"""
from dataclasses import field
from typing import List
from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass

# -------------------------------------------------------------------------


@dataclass
class MessageFrom:
    """MessageFrom class represents a user sent a message"""

    id: int
    first_name: str
    username: str
    last_name: str = ""

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    """Chat class represents chat the message was sent from"""

    id: int
    type: str
    first_name: str
    username: str
    last_name: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    """Message class represents a message"""

    message_id: int
    chat: Chat
    text: str
    from_: MessageFrom = field(metadata={"data_key": "from"})

    class Meta:
        unknown = EXCLUDE


@dataclass
class Update:
    """Update class represents an update data of the response"""

    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    """GetUpdatesResponse class represents a getUpdate response received
    from the telegram bot API"""

    ok: bool
    result: List[Update]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    """GetUpdatesResponse class represents a sendMessage response received
    from the telegram bot API"""

    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
