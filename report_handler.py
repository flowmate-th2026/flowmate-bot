from report_service import get_daily_sales_report


def handle_report_message():
    """
    ดึงข้อมูลและสร้างข้อความรายงานประจำวัน
    """

    try:
        report = get_daily_sales_report()

        total_sales = report["total_sales"]
        total_expenses = report["total_expenses"]
        profit = report["profit"]
        transaction_count = report["transaction_count"]
        average_sales = report["average_sales"]
        latest_sales = report["latest_sales"]
        latest_expenses = report["latest_expenses"]
        total_customers = report["total_customers"]
        average_sales_per_customer = report["average_sales_per_customer"]
        total_product_quantity = report["total_product_quantity"]
        product_transaction_count = report["product_transaction_count"]
        top_products = report["top_products"]

        latest_sales_text = ""

        for item in latest_sales:
            latest_sales_text += (
                f"• {item['time']} — "
                f"{item['amount']:,.2f} บาท\n"
            )

        latest_expenses_text = ""

        for item in latest_expenses:
            latest_expenses_text += (
                f"• {item['time']} — "
                f"{item['amount']:,.2f} บาท "
                f"({item['description']})\n"
            )

        top_products_text = ""

        for index, item in enumerate(top_products, start=1):
            top_products_text += (
                f"{index}. {item['product_name']} — "
                f"{item['quantity']:,} ชิ้น "
                f"({item['amount']:,.2f} บาท)\n"
            )

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

         reply = (
            "📊 สรุปร้านค้าประจำวัน\n"
            f"📅 {report['date']}\n\n"
            "──────────────\n\n"
            "💰 ยอดขาย\n"
            f"{total_sales:,.2f} บาท\n\n"
            "💸 ค่าใช้จ่าย\n"
            f"{total_expenses:,.2f} บาท\n\n"
            f"{profit_text}\n\n"
            "──────────────\n\n"
            f"👥 ลูกค้าทั้งหมด: {total_customers:,} คน\n"
            f"🧾 รายการขาย: {transaction_count:,} รายการ\n"
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
                "ยังไม่มีข้อมูลสินค้าที่ขายวันนี้"
            )

        if latest_sales_text:
            reply += (
                "\n\n🕒 ยอดขายล่าสุด\n"
                f"{latest_sales_text.rstrip()}"
            )

        if latest_expenses_text:
            reply += (
                "\n\n💸 ค่าใช้จ่ายล่าสุด\n"
                f"{latest_expenses_text.rstrip()}"
            )

        return reply

    except Exception as error:
        print(f"เกิดข้อผิดพลาดใน report_handler.py: {error}")

        return (
            "⚠️ ระบบยังเปิดรายงานไม่ได้ในขณะนี้\n\n"
            "กรุณาลองใหม่อีกครั้ง"
        )
