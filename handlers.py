from datetime import datetime
from zoneinfo import ZoneInfo

from linebot.models import TextSendMessage


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
                thailand_time = datetime.now(ZoneInfo("Asia/Bangkok"))

                if amount.is_integer():
                    formatted_amount = f"{amount:,.0f}"
                else:
                    formatted_amount = f"{amount:,.2f}"

                reply = (
                    "✅ บันทึกยอดขายเรียบร้อย\n\n"
                    f"📅 วันที่: {thailand_time.strftime('%d/%m/%Y')}\n"
                    f"⏰ เวลา: {thailand_time.strftime('%H:%M')}\n"
                    f"💰 ยอดขาย: {formatted_amount} บาท"
                )

        except ValueError:
            reply = (
                "❌ รูปแบบยอดขายไม่ถูกต้อง\n\n"
                "กรุณาพิมพ์ตัวเลข เช่น:\n"
                "ยอดขาย 2500"
            )

    elif normalized_message == "รายงาน":
        reply = (
            "📊 ระบบรายงานร้านค้า\n\n"
            "ขณะนี้ยังไม่มีข้อมูลยอดขายที่บันทึกถาวร\n"
            "ขั้นต่อไปเราจะเชื่อม Google Sheets ค่ะ"
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
