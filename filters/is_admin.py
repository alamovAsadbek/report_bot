from aiogram import types
from aiogram.filters import Filter
from os import getenv
from typing import List


class IsAdminFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        admin_ids = self._get_admin_ids()
        return message.from_user.id in admin_ids
    
    @staticmethod
    def _get_admin_ids() -> List[int]:
        admins = getenv("ADMINS", "").split(",")
        return [int(admin_id) for admin_id in admins if admin_id.strip()]
