from linebot.models import TextSendMessage

from services import (
    record_sale,
    record_expense,
    get_daily_sales_report,
)

def handle_text_message(event, line_bot_api):
    user_message = event.message.text.strip()
    normalized_message = user_message.lower()

    if normalized_message in ["สวัสดี", "หวัดดี", "hello", "hi"]:
        reply = (
            "👋 สวัสดีค่ะ ยินดีต้อนรับสู่ FlowMate\n\n"
            "พิมพ์คำว่า “เมนู” เพื่อดูคำสั่งทั้งหมด"
        )

    elif normalized_message in ["เมนู", "menu"]:
        reply = (
            "🤖 เมนู FlowMate\n\n"
            "1️⃣ พิมพ์ “ยอดขาย 2500” เพื่อบันทึกยอดขาย\n"
            "2️⃣ พิมพ์ “รายงาน” เพื่อดูรายงานร้านค้า\n"
            "3️⃣ พิมพ์ “ช่วยเหลือ” เพื่อดูวิธีใช้งาน"
        )

    elif normalized_message == "ยอดขาย":
        reply = (
            "💰 กรุณาใส่จำนวนเงินต่อท้ายคำว่ายอดขาย\n\n"
            "ตัวอย่าง:\n"
            "ยอดขาย 2500"
        )

    elif normalized_message.startswith("ยอดขาย "):
        amount_text = user_message.replace("ยอดขาย", "", 1).strip()
        amount_text = amount_text.replace(",", "")

        try:
            amount = float(amount_text)

            if amount <= 0:
                reply = "❌ ยอดขายต้องมากกว่า 0 บาท"
            else:
                date_text, time_text = record_sale(amount)

                if amount.is_integer():
                    formatted_amount = f"{amount:,.0f}"
                else:
                    formatted_amount = f"{amount:,.2f}"

                reply = (
                    "✅ บันทึกยอดขายลง Google Sheets เรียบร้อย\n\n"
                    f"📅 วันที่: {date_text}\n"
                    f"⏰ เวลา: {time_text}\n"
                    f"💰 ยอดขาย: {formatted_amount} บาท"
                )
    elif normalized_message == "ค่าใช้จ่าย":
        reply = (
            "💸 กรุณาใส่จำนวนเงินและรายละเอียด\n\n"
            "ตัวอย่าง:\n"
            "ค่าใช้จ่าย 350 ค่านม"
        )

    elif normalized_message.startswith("ค่าใช้จ่าย "):
        expense_text = user_message.replace("ค่าใช้จ่าย", "", 1).strip()
        expense_parts = expense_text.split(maxsplit=1)

        if not expense_parts:
            reply = (
                "❌ รูปแบบค่าใช้จ่ายไม่ถูกต้อง\n\n"
                "ตัวอย่าง:\n"
                "ค่าใช้จ่าย 350 ค่านม"
            )

        else:
            amount_text = expense_parts[0].replace(",", "")

            if len(expense_parts) > 1:
                description = expense_parts[1].strip()
            else:
                description = "ไม่ระบุรายละเอียด"

            try:
                amount = float(amount_text)

                if amount <= 0:
                    reply = "❌ ค่าใช้จ่ายต้องมากกว่า 0 บาท"
                else:
                    date_text, time_text = record_expense(
                        amount,
                        description,
                    )

                    if amount.is_integer():
                        formatted_amount = f"{amount:,.0f}"
                    else:
                        formatted_amount = f"{amount:,.2f}"

                    reply = (
                        "✅ บันทึกค่าใช้จ่ายเรียบร้อย\n\n"
                        f"📅 วันที่: {date_text}\n"
                        f"⏰ เวลา: {time_text}\n"
                        f"💸 ค่าใช้จ่าย: {formatted_amount} บาท\n"
                        f"📝 รายละเอียด: {description}"
                    )

            except ValueError:
                reply = (
                    "❌ รูปแบบค่าใช้จ่ายไม่ถูกต้อง\n\n"
                    "กรุณาพิมพ์ตัวเลข เช่น:\n"
                    "ค่าใช้จ่าย 350 ค่านม"
                )

            except Exception:
                reply = (
                    "⚠️ ระบบยังบันทึกค่าใช้จ่ายไม่ได้ในขณะนี้\n\n"
                    "กรุณาลองใหม่อีกครั้ง"
                )
    
    elif normalized_message in ["รายงาน", "สรุปวันนี้"]:
        try:
            report = get_daily_sales_report()

            total_sales = report["total_sales"]
            transaction_count = report["transaction_count"]
            average_sales = report["average_sales"]
            latest_sales = report["latest_sales"]

            if transaction_count == 0:
                reply = (
                    "📊 รายงานยอดขายวันนี้\n"
                    f"📅 {report['date']}\n\n"
                    "วันนี้ยังไม่มียอดขายที่บันทึกไว้ค่ะ\n\n"
                    "พิมพ์ตัวอย่าง:\n"
                    "ยอดขาย 500"
                )

            else:
                latest_text = ""

                for item in latest_sales:
                    latest_text += (
                        f"• {item['time']} — "
                        f"{item['amount']:,.2f} บาท\n"
                    )

                reply = (
                    "📊 รายงานยอดขายวันนี้\n"
                    f"📅 {report['date']}\n\n"
                    f"💰 ยอดขายรวม: {total_sales:,.2f} บาท\n"
                    f"🧾 จำนวนรายการ: {transaction_count} รายการ\n"
                    f"📈 ยอดขายเฉลี่ย: {average_sales:,.2f} บาท\n\n"
                    "🕒 รายการล่าสุด\n"
                    f"{latest_text}"
                )

        except Exception:
            reply = (
                "⚠️ ระบบยังเปิดรายงานไม่ได้ในขณะนี้\n\n"
                "กรุณาลองใหม่อีกครั้ง"
            )

    elif normalized_message == "ช่วยเหลือ":
        reply = (
            "🆘 วิธีใช้งาน FlowMate\n\n"
            "• เมนู\n"
            "• ยอดขาย 2500\n"
            "• รายงาน\n"
            "• ช่วยเหลือ"
        )

    else:
        reply = (
            "ขออภัยค่ะ FlowMate ยังไม่เข้าใจข้อความนี้\n\n"
            "พิมพ์คำว่า “เมนู” เพื่อดูคำสั่งที่ใช้ได้"
        )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )
