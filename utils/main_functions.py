from datetime import datetime
from main.constants import ReportType
import pytz

from utils.more_functions import change_date_format


from datetime import datetime
import pytz

def change_utc_to_local(utc_time):
    utc_datetime = datetime.fromisoformat(utc_time).replace(tzinfo=pytz.UTC)

    tashkent_tz = pytz.timezone('Asia/Tashkent')

    tashkent_time = utc_datetime.astimezone(tashkent_tz)

    return tashkent_time.strftime("%Y-%m-%d %H:%M:%S")



def change_amount_to_number(amount_to_number):
    # Agar son float bo'lsa, oxirgi nol va nuqtani olib tashlash
    if isinstance(amount_to_number, float):
        amount_to_number = str(amount_to_number).rstrip('0').rstrip('.')  # Oxirgi 0 larni olib tashlash

    # Sonni formatlash va vergulni bo'sh joy bilan almashtirish
    report_summ = "{:,.0f}".format(float(amount_to_number)).replace(",", " ")
    return report_summ


def change_amount_to_string(amount_to_number):
    amount = f"{amount_to_number:,.2f}".replace(",", " ").__str__()
    return amount


def create_report(data):
    report_text = str()
    report_summ = 0
    report_text += f"\n 📝 Jami hisobotlar soni: {len(data)} ta\n\n"
    for index, report in enumerate(data):
        new_amount = f"{int(report['amount']):,}".replace(",", " ")
        created_at = change_utc_to_local(str(report['created_at']))
        report_text += f"{index + 1}. {str(new_amount)} so'm, {report['description']}, {change_date_format(created_at)}" + "\n \n"
        report_summ += report['amount']
    report_summ = change_amount_to_number(report_summ)
    print('summ: ', report_summ * 1)
    report_text += f"✅ Umumiy hisob: {report_summ} so'm"

    return_data = {
        "report_text": report_text,
        "report_summ": report_summ
    }
    return return_data


def create_global_report(data):
    report_text = str()
    report_summ = 0
    report_text += f"\n 📝 Jami hisobotlar soni: {len(data)} ta\n\n"
    for index, report in enumerate(data):
        new_amount = f"{int(report['amount']):,}".replace(",", " ")
        created_at = change_utc_to_local(str(report['created_at']))
        if report['type'] == ReportType.income.value:
            report_summ += report['amount']
            report_text += f"{index + 1}. Daromad, {str(new_amount)} so'm, {report['description']}, {change_date_format(created_at)}" + "\n \n"
        elif report['type'] == ReportType.expense.value:
            report_text += f"{index + 1}. Xarajat, {str(new_amount)} so'm, {report['description']}, {change_date_format(created_at)}" + "\n \n"
            report_summ -= report['amount']
    report_summ = change_amount_to_number(report_summ)
    print("global report summ:", report_summ)
    report_text += f"✅ Umumiy hisob: {report_summ} so'm"
    return_data = {
        "report_text": report_text,
        "report_summ": report_summ
    }
    return return_data
