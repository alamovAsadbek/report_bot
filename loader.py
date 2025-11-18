from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n

from main import config
from main.config import LOCALES_DIR, I18N_DOMAIN

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

i18n = I18n(path=LOCALES_DIR, default_locale="en", domain=I18N_DOMAIN)
_ = i18n.gettext
