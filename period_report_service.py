from datetime import timedelta

from report_service import get_thailand_time
from sheet_service import get_rows_by_date_range


def build_period_report(start_date, end_date):
    """
    คำนวณรายงานจากข้อมูลในช่วงวันที่กำหนด
    """

    rows = get_rows_by_date_range(
        start_date=start_date,
        end_date=end_date,
    )

    total_sales = 0
    total_expenses = 0
    total_customers = 0
    total_product_quantity = 0

    sales_transaction_count = 0
    product_transaction_count = 0

    product_summary = {}

    for row in rows:
        row_type = str(
            row.get("ประเภท", "")
        ).strip()

        amount_text = str(
            row.get("จำนวนเงิน", "0")
        )
        amount_text = amount_text.replace(",", "").strip()

        try:
            amount = float(amount_text)
        except (ValueError, TypeError):
            amount = 0

        if row_type == "ยอดขาย":
            if amount > 0:
                total_sales += amount
                sales_transaction_count += 1

        elif row_type == "ค่าใช้จ่าย":
            if amount > 0:
                total_expenses += amount

        elif row_type == "ลูกค้า":
            try:
                customer_count = int(float(amount_text))
            except (ValueError, TypeError):
                customer_count = 0

            if customer_count > 0:
                total_customers += customer_count

        elif row_type == "ขายสินค้า":
            product_name = str(
                row.get("ชื่อสินค้า", "")
            ).strip()

            quantity_text = str(
                row.get("จำนวนขาย", "0")
            )
            quantity_text = quantity_text.replace(",", "").strip()

            try:
                quantity = int(float(quantity_text))
            except (ValueError, TypeError):
                quantity = 0

            if (
                product_name
                and quantity > 0
                and amount > 0
            ):
                total_product_quantity += quantity
                product_transaction_count += 1

                normalized_product_name = product_name.lower()

                if normalized_product_name not in product_summary:
                    product_summary[normalized_product_name] = {
                        "product_name": product_name,
                        "quantity": 0,
                        "amount": 0,
                    }

                product_summary[
                    normalized_product_name
                ]["quantity"] += quantity

                product_summary[
                    normalized_product_name
                ]["amount"] += amount

    profit = total_sales - total_expenses

    if sales_transaction_count > 0:
        average_sales = (
            total_sales / sales_transaction_count
        )
    else:
        average_sales = 0

    if total_customers > 0:
        average_sales_per_customer = (
            total_sales / total_customers
        )
    else:
        average_sales_per_customer = 0

    top_products = sorted(
        product_summary.values(),
        key=lambda item: (
            item["quantity"],
            item["amount"],
        ),
        reverse=True,
    )[:3]

    return {
        "start_date": start_date.strftime("%d/%m/%Y"),
        "end_date": end_date.strftime("%d/%m/%Y"),
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "profit": profit,
        "total_customers": total_customers,
        "sales_transaction_count": sales_transaction_count,
        "average_sales": average_sales,
        "average_sales_per_customer": average_sales_per_customer,
        "total_product_quantity": total_product_quantity,
        "product_transaction_count": product_transaction_count,
        "top_products": top_products,
    }


def get_weekly_report():
    """
    รายงานตั้งแต่วันจันทร์จนถึงวันนี้
    """

    today = get_thailand_time().date()
    start_date = today - timedelta(
        days=today.weekday()
    )

    return build_period_report(
        start_date=start_date,
        end_date=today,
    )


def get_monthly_report():
    """
    รายงานตั้งแต่วันที่ 1 ของเดือนจนถึงวันนี้
    """

    today = get_thailand_time().date()
    start_date = today.replace(day=1)

    return build_period_report(
        start_date=start_date,
        end_date=today,
    )
