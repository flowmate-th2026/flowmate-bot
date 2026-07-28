from datetime import datetime
from zoneinfo import ZoneInfo

from sheet_service import (
    append_sale_row,
    append_expense_row,
    get_sales_rows_by_date,
    get_expense_rows_by_date,
)

def get_thailand_time():
    return datetime.now(ZoneInfo("Asia/Bangkok"))


def record_sale(amount):
    thailand_time = get_thailand_time()

    date_text = thailand_time.strftime("%d/%m/%Y")
    time_text = thailand_time.strftime("%H:%M")

    append_sale_row(
        date_text=date_text,
        time_text=time_text,
        amount=amount,
    )
    
    return date_text, time_text

def record_expense(amount, description):
    thailand_time = get_thailand_time()

    date_text = thailand_time.strftime("%d/%m/%Y")
    time_text = thailand_time.strftime("%H:%M")

    append_expense_row(
        date_text=date_text,
        time_text=time_text,
        amount=amount,
        description=description,
    )

    return date_text, time_text
    
def get_daily_sales_report():
    thailand_time = get_thailand_time()
    date_text = thailand_time.strftime("%d/%m/%Y")

    sales_rows = get_sales_rows_by_date(date_text)

    valid_sales = []

    for row in sales_rows:
        amount_text = str(row.get("จำนวนเงิน", "0"))
        amount_text = amount_text.replace(",", "").strip()

        try:
            amount = float(amount_text)
        except ValueError:
            continue

        valid_sales.append(
            {
                "time": str(row.get("เวลา", "")).strip(),
                "amount": amount,
            }
        )

    total_sales = sum(item["amount"] for item in valid_sales)
    transaction_count = len(valid_sales)

    if transaction_count > 0:
        average_sales = total_sales / transaction_count
    else:
        average_sales = 0

    latest_sales = list(reversed(valid_sales[-3:]))

    return {
        "date": date_text,
        "total_sales": total_sales,
        "transaction_count": transaction_count,
        "average_sales": average_sales,
        "latest_sales": latest_sales,
    }
