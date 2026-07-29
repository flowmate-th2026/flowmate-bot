from services import (
    get_daily_sales,
    get_daily_expense,
    get_daily_customer,
)

from report_flex import create_report_flex


def handle_report_message():
    """
    สร้างรายงานประจำวันในรูปแบบ Flex Message
    """

    sales = get_daily_sales()
    expense = get_daily_expense()
    customer = get_daily_customer()

    profit = sales - expense

    return create_report_flex(
        sales=sales,
        expense=expense,
        customer=customer,
        profit=profit,
    )
