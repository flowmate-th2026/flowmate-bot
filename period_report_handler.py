from period_report_service import (
    get_monthly_report,
    get_weekly_report,
)


def format_period_report(report, report_title):
    """
    จัดรูปแบบข้อความรายงานตามช่วงเวลา
    """

    total_sales = report["total_sales"]
    total_expenses = report["total_expenses"]
    profit = report["profit"]
    total_customers = report["total_customers"]
    sales_transaction_count = report["sales_transaction_count"]
    average_sales = report["average_sales"]
    average_sales_per_customer = report[
        "average_sales_per_customer"
    ]
    total_product_quantity = report["total_product_quantity"]
    product_transaction_count = report[
        "product_transaction_count"
    ]
    top_products = report["top_products"]

    if profit >= 0:
        profit_text = (
            "💵 กำไรสุทธิ\n"
            f"{profit:,.2f} บาท"
        )
    else:
        profit_text = (
            "🔻 ขาดทุนสุทธิ\n"
            f"{abs(profit):,.2f} บาท"
        )

    top_products_text = ""

    for index, item in enumerate(top_products, start=1):
        top_products_text += (
            f"{index}. {item['product_name']} — "
            f"{item['quantity']:,} ชิ้น "
            f"({item['amount']:,.2f} บาท)\n"
        )

    reply = (
        f"📊 {report_title}\n"
        f"📅 {report['start_date']} - "
        f"{report['end_date']}\n\n"
        "──────────────\n\n"
        "💰 ยอดขายรวม\n"
        f"{total_sales:,.2f} บาท\n\n"
        "💸 ค่าใช้จ่ายรวม\n"
        f"{total_expenses:,.2f} บาท\n\n"
        f"{profit_text}\n\n"
        "──────────────\n\n"
        f"👥 ลูกค้าทั้งหมด: {total_customers:,} คน\n"
        f"🧾 รายการขาย: "
        f"{sales_transaction_count:,} รายการ\n"
        f"🛒 ยอดเฉลี่ยต่อลูกค้า: "
        f"{average_sales_per_customer:,.2f} บาท\n"
        f"📈 ยอดเฉลี่ยต่อรายการ: "
        f"{average_sales:,.2f} บาท\n\n"
        "──────────────\n\n"
        f"🛍️ สินค้าที่ขายทั้งหมด: "
        f"{total_product_quantity:,} ชิ้น\n"
        f"🧾 รายการขายสินค้า: "
        f"{product_transaction_count:,} รายการ"
    )

    if top_products_text:
        reply += (
            "\n\n🏆 Top 3 สินค้าขายดี\n"
            f"{top_products_text.rstrip()}"
        )
    else:
        reply += (
            "\n\n🏆 Top 3 สินค้าขายดี\n"
            "ยังไม่มีข้อมูลสินค้าที่ขายในช่วงนี้"
        )

    return reply


def handle_weekly_report_message():
    """
    สร้างข้อความรายงานประจำสัปดาห์
    """

    try:
        report = get_weekly_report()

        return format_period_report(
            report=report,
            report_title="สรุปร้านค้าประจำสัปดาห์",
        )

    except Exception as error:
        print(
            f"เกิดข้อผิดพลาดในรายงานสัปดาห์: {error}",
            flush=True,
        )

        return (
            "⚠️ ระบบยังเปิดรายงานสัปดาห์ไม่ได้ในขณะนี้\n\n"
            "กรุณาลองใหม่อีกครั้ง"
        )


def handle_monthly_report_message():
    """
    สร้างข้อความรายงานประจำเดือน
    """

    try:
        report = get_monthly_report()

        return format_period_report(
            report=report,
            report_title="สรุปร้านค้าประจำเดือน",
        )

    except Exception as error:
        print(
            f"เกิดข้อผิดพลาดในรายงานเดือน: {error}",
            flush=True,
        )

        return (
            "⚠️ ระบบยังเปิดรายงานเดือนไม่ได้ในขณะนี้\n\n"
            "กรุณาลองใหม่อีกครั้ง"
        )
