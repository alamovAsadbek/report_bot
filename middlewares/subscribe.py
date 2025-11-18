from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.enums import ChatMemberStatus as CHatS
from aiogram.types import Message

from loader import bot
from logging_settings import logger


class SubscribeMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        user_id = event.from_user.id
        channel_id = -1002110742395
        try:
            # if handler in ['start']:
            #     return await handler(event, data)
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status in [CHatS.CREATOR, CHatS.ADMINISTRATOR, CHatS.MEMBER]:
                return await handler(event, data)
            else:
                await bot.send_message(text="Not joined", chat_id=user_id)
        except Exception as e:
            logger.error(e)
            return await handler(event, data)
