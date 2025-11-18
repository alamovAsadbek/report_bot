from aiogram import Bot

from logging_settings import logger
from main.config import DEVS


async def send_notification_to_devs(bot: Bot):
    try:
        for dev in DEVS:
            await bot.send_message(text="Bot start to work", chat_id=dev)
    except Exception as e:
        logger.error(f"While sending info to devs: {e}")
