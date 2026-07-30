from services import (
    get_daily_sales,
    get_daily_expense,
    get_daily_customer,
    get_thailand_time,
)

from product_handler import get_top_products_data
from report_flex import create_report_flex


def handle_report_message():
    """
    สร้างรายงานประจำวันในรูปแบบ Flex Message
    """

    sales = get_daily_sales()
    expense = get_daily_expense()
    customer = get_daily_customer()

    now = get_thailand_time()
    date_text = now.strftime("%d/%m/%Y")
    top_products = get_top_products_data(date_text, limit=3)

    profit = sales - expense

    return create_report_flex(
    sales=sales,
    expense=expense,
    customer=customer,
    profit=profit,
    top_products=top_products,
)
