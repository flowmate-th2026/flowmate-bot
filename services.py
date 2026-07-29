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

def get_daily_sales_report():
    thailand_time = get_thailand_time()
    date_text = thailand_time.strftime("%d/%m/%Y")

    sales_rows = get_sales_rows_by_date(date_text)
    expense_rows = get_expense_rows_by_date(date_text)
    customer_rows = get_customer_rows_by_date(date_text)

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

    valid_expenses = []

    for row in expense_rows:
        amount_text = str(row.get("จำนวนเงิน", "0"))
        amount_text = amount_text.replace(",", "").strip()

        try:
            amount = float(amount_text)
        except ValueError:
            continue

        valid_expenses.append(
            {
                "time": str(row.get("เวลา", "")).strip(),
                "amount": amount,
                "description": str(
                    row.get("รายละเอียด", "")
                ).strip(),
            }
        )

    valid_customers = []

    for row in customer_rows:
        customer_text = str(row.get("จำนวนเงิน", "0"))
        customer_text = customer_text.replace(",", "").strip()

        try:
            customer_count = int(float(customer_text))
        except ValueError:
            continue

        if customer_count <= 0:
            continue

        valid_customers.append(
            {
                "time": str(row.get("เวลา", "")).strip(),
                "customer_count": customer_count,
            }
        )

    total_sales = sum(
        item["amount"] for item in valid_sales
    )

    total_expenses = sum(
        item["amount"] for item in valid_expenses
    )

    total_customers = sum(
        item["customer_count"] for item in valid_customers
    )

    profit = total_sales - total_expenses
    transaction_count = len(valid_sales)

    if transaction_count > 0:
        average_sales = total_sales / transaction_count
    else:
        average_sales = 0

    if total_customers > 0:
        average_sales_per_customer = total_sales / total_customers
    else:
        average_sales_per_customer = 0

    latest_sales = list(reversed(valid_sales[-3:]))
    latest_expenses = list(reversed(valid_expenses[-3:]))
    latest_customers = list(reversed(valid_customers[-3:]))

    return {
        "date": date_text,
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "profit": profit,
        "transaction_count": transaction_count,
        "average_sales": average_sales,
        "total_customers": total_customers,
        "average_sales_per_customer": average_sales_per_customer,
        "latest_sales": latest_sales,
        "latest_expenses": latest_expenses,
        "latest_customers": latest_customers,
    }
