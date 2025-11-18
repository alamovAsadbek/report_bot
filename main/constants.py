from enum import Enum


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class ReportStatus(str, Enum):
    deactivated = "deactivated"
    activated = "activated"

class ReportType(str, Enum):
    income = "income"
    expense = "expense"
