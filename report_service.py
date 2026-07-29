from datetime import datetime
from zoneinfo import ZoneInfo

from sheet_service import (
    get_sales_rows_by_date,
    get_expense_rows_by_date,
    get_customer_rows_by_date,
    get_product_rows_by_date,
)

def get_thailand_time():
    """
    คืนค่าวันและเวลาปัจจุบันตามประเทศไทย
    """
    return datetime.now(ZoneInfo("Asia/Bangkok"))


def get_daily_sales_report():
    """
    อ่านข้อมูลประจำวันจาก Google Sheets
    และคำนวณรายงานยอดขาย ค่าใช้จ่าย กำไร และลูกค้า
    """

    thailand_time = get_thailand_time()
    date_text = thailand_time.strftime("%d/%m/%Y")

    sales_rows = get_sales_rows_by_date(date_text)
    expense_rows = get_expense_rows_by_date(date_text)
    customer_rows = get_customer_rows_by_date(date_text)
    product_row = get_product_rows_by_date(date_text)

    valid_sales = []

    for row in sales_rows:
        amount_text = str(row.get("จำนวนเงิน", "0"))
        amount_text = amount_text.replace(",", "").strip()

        try:
            amount = float(amount_text)
        except (ValueError, TypeError):
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
        except (ValueError, TypeError):
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
        except (ValueError, TypeError):
            continue

        if customer_count <= 0:
            continue

        valid_customers.append(
            {
                "time": str(row.get("เวลา", "")).strip(),
                "customer_count": customer_count,
            }
        )

    valid_products = []

    for row in product_rows:
        product_name = str(
            row.get("ชื่อสินค้า", "")
        ).strip()

        quantity_text = str(
            row.get("จำนวนขาย", "0")
        )
        quantity_text = quantity_text.replace(",", "").strip()

        amount_text = str(
            row.get("จำนวนเงิน", "0")
        )
        amount_text = amount_text.replace(",", "").strip()

        try:
            quantity = int(float(quantity_text))
            amount = float(amount_text)
        except (ValueError, TypeError):
            continue

        if not product_name:
            continue

        if quantity <= 0 or amount <= 0:
            continue

        valid_products.append(
            {
                "product_name": product_name,
                "quantity": quantity,
                "amount": amount,
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
    
     total_product_quantity = sum(
        item["quantity"] for item in valid_products
    )

    product_summary = {}

    for item in valid_products:
        product_name = item["product_name"]
        normalized_product_name = product_name.lower()

        if normalized_product_name not in product_summary:
            product_summary[normalized_product_name] = {
                "product_name": product_name,
                "quantity": 0,
                "amount": 0,
            }

        product_summary[normalized_product_name]["quantity"] += (
            item["quantity"]
        )

        product_summary[normalized_product_name]["amount"] += (
            item["amount"]
        )

    top_products = sorted(
        product_summary.values(),
        key=lambda item: (
            item["quantity"],
            item["amount"],
        ),
        reverse=True,
    )[:3]

    profit = total_sales - total_expenses
    transaction_count = len(valid_sales)

    if transaction_count > 0:
        average_sales = total_sales / transaction_count
    else:
        average_sales = 0

    if total_customers > 0:
        average_sales_per_customer = (
            total_sales / total_customers
        )
    else:
        average_sales_per_customer = 0

    latest_sales = list(
        reversed(valid_sales[-3:])
    )

    latest_expenses = list(
        reversed(valid_expenses[-3:])
    )

    latest_customers = list(
        reversed(valid_customers[-3:])
    )

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
        "total_product_quantity": total_product_quantity,
        "product_transaction_count": len(valid_products),
        "top_products": top_products,
    }
