from datetime import datetime
from typing import Union, List

from aiogram import types
from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload
from logging_settings import logger
from main.constants import UserStatus, ReportType, ReportStatus
from main.database import database
from main.models import User, Report


async def get_user(chat_id: int) -> Union[dict, None]:
    try:
        query = select(User).where(User.chat_id == chat_id)
        row = await database.fetch_one(query)
        return dict(row._mapping) if row else None
    except Exception as e:
        logger.error(f"Error retrieving user with ID {chat_id}: {e}")
        return None


async def add_user(message: types.Message, data: dict) -> Union[int, None]:
    try:
        query = insert(User).values(
            chat_id=message.chat.id,
            full_name=data.get("full_name"),
            phone_number=data.get("phone_number"),
            language=data.get("language"),
            username=message.from_user.username,
            status=UserStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        new_user_id = await database.execute(query)
        return new_user_id
    except Exception as e:
        logger.error(f"Error adding new user {message.chat.id}: {e}")
        return None


async def add_income_and_expense_reports(message: types.Message, data: dict) -> Union[int, None]:
    try:
        query = insert(Report).values(
            telegram_id=message.chat.id,
            amount=int(data.get("amount")),
            description=data.get("description"),
            type=data.get("type"),
            status=data.get("status"),
            created_at=message.date,
            updated_at=message.date
        ).returning(Report.id)
        new_income = await database.execute(query)
        return new_income
    except Exception as e:
        logger.error(f"Error adding income report for user {message.chat.id}: {e}")
        return None


async def get_user_income_and_expense_reports(chat_id: int, report_type: ReportType = None,
                                              filter_date: datetime = None) -> Union[List[dict], None]:
    try:
        stmt = select(Report).where(
            Report.telegram_id == chat_id,
            Report.status == ReportStatus.activated.value
        )

        if report_type:
            stmt = stmt.where(Report.type == report_type)
        if filter_date:
            stmt = stmt.where(Report.created_at >= filter_date)

        stmt = stmt.order_by(Report.created_at.desc())

        rows = await database.fetch_all(stmt)
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        logger.error(f"Error retrieving reports for user {chat_id}: {e}")
        return None


async def get_one_report(data_id: int) -> Union[dict, None]:
    try:
        stmt = select(Report).where(
            Report.id == data_id,
            Report.status == ReportStatus.activated.value
        )
        row = await database.fetch_one(stmt)
        return dict(row._mapping) if row else None
    except Exception as e:
        logger.error(f"Error retrieving report with ID {data_id}: {e}")
        return None


async def update_status_report(data_id: int) -> Union[bool, None]:
    try:
        stmt = update(Report).where(Report.id == data_id).values(
            status=ReportStatus.deactivated.value
        )
        updated = await database.execute(stmt)
        return updated > 0
    except Exception as e:
        logger.error(f"Error updating report with ID {data_id}: {e}")
        return None
