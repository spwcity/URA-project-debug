import json

import aiormq
from loguru import logger

from . import base


async def send_message(send_to: int, forward_message_chat: int, forward_message: int, priority: int = 0):
    channel = await base.connection.channel()

    body = json.dumps({
        "send_to": send_to,
        "forward_message_chat": forward_message_chat,
        "forward_message": forward_message,

    }, separators=(',', ':')).encode()

    await channel.basic_publish(
        body,
        routing_key='send_message',
        properties=aiormq.spec.Basic.Properties(priority=priority)
    )

    logger.debug(
        f'Booked message to {send_to} from chat {forward_message_chat} message {forward_message} prioriy {priority}.')

