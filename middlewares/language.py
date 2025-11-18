from aiogram.utils.i18n import I18nMiddleware

from utils.db_commands.user import get_user


async def get_lang(user_id):
    user = await get_user(user_id)
    return user.get("uz") if user else "uz"


class LanguageMiddleware(I18nMiddleware):

    async def get_locale(self, event, data) -> str:
        user = getattr(event, "from_user", data.get("event_from_user"))
        return "uz"
