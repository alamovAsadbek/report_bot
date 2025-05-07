# main/models.py

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from main.constants import UserStatus, ReportType, ReportStatus

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    language = Column(String, nullable=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    status = Column(String, default=UserStatus.active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)


class Report(Base):
    __tablename__ = "reports"

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False)
    amount = Column(DECIMAL, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, default=ReportType.income, nullable=False)
    status = Column(String, default=ReportStatus.activated, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
