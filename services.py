from datetime import datetime
from zoneinfo import ZoneInfo

from sheet_service import append_sale_row


def record_sale(amount):
    thailand_time = datetime.now(ZoneInfo("Asia/Bangkok"))

    date_text = thailand_time.strftime("%d/%m/%Y")
    time_text = thailand_time.strftime("%H:%M")

    append_sale_row(
        date_text=date_text,
        time_text=time_text,
        amount=amount,
    )

    return date_text, time_text
