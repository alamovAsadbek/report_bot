from datetime import datetime


def change_date_format(deformat_date: str = datetime.now()):
    dt = datetime.strptime(deformat_date, "%Y-%m-%d %H:%M:%S")
    format_date = dt.strftime("%d.%m.%Y %H:%M")
    return format_date
