from datetime import datetime
from zoneinfo import ZoneInfo

from sheet_service import (
    append_sale_row,
    append_expense_row,
    append_customer_row,
    append_product_row,
    get_sales_rows_by_date,
    get_expense_rows_by_date,
    get_customer_rows_by_date,
)

def get_thailand_time():
    return datetime.now(ZoneInfo("Asia/Bangkok"))


def record_sale(
    amount,
    sheet_id=None,
):
    now = get_thailand_time()
    date_text = now.strftime("%d/%m/%Y")
    time_text = now.strftime("%H:%M")

    append_sale_row(
        date_text,
        time_text,
        amount,
        sheet_id=sheet_id,
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

def record_customer(customer_count):
    thailand_time = get_thailand_time()

    date_text = thailand_time.strftime("%d/%m/%Y")
    time_text = thailand_time.strftime("%H:%M")

    append_customer_row(
        date_text=date_text,
        time_text=time_text,
        customer_count=customer_count,
    )

    return date_text, time_text

def record_product(product_name, quantity, amount):
    thailand_time = get_thailand_time()

    date_text = thailand_time.strftime("%d/%m/%Y")
    time_text = thailand_time.strftime("%H:%M")

    append_product_row(
        date_text=date_text,
        time_text=time_text,
        product_name=product_name,
        quantity=quantity,
        amount=amount,
    )

    return date_text, time_text

def get_daily_sales():
    today = get_thailand_time().strftime("%d/%m/%Y")
    rows = get_sales_rows_by_date(today)

    total = 0

    for row in rows:
        total += float(row.get("จำนวนเงิน", 0))

    return total

def get_daily_expense():
    today = get_thailand_time().strftime("%d/%m/%Y")
    rows = get_expense_rows_by_date(today)

    total = 0

    for row in rows:
        total += float(row.get("จำนวนเงิน", 0))

    return total

def get_daily_customer():
    today = get_thailand_time().strftime("%d/%m/%Y")
    rows = get_customer_rows_by_date(today)

    total = 0

    for row in rows:
        total += int(row.get("จำนวนลูกค้า", 0))

    return total
