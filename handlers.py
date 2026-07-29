from linebot.models import TextSendMessage

from customer_handler import handle_customer_message
from expense_handler import handle_expense_message
from menu_handler import handle_menu_message
from period_report_handler import (
    handle_monthly_report_message,
    handle_weekly_report_message,
)
from product_handler import handle_product_message
from report_handler import handle_report_message
from sales_handler import handle_sales_message


def handle_text_message(event, line_bot_api):
    """
    รับข้อความจาก LINE แล้วส่งต่อไปยัง handler ที่เกี่ยวข้อง
    """

    user_message = event.message.text.strip()
    normalized_message = user_message.lower()

    try:
        # เมนู คำทักทาย วิธีใช้งาน และปุ่มในการ์ดยอดขาย
        if normalized_message in [
            "สวัสดี",
            "หวัดดี",
            "hello",
            "hi",
            "เมนู",
            "menu",
            "ช่วยเหลือ",
            "ยอดขาย",
            "กรอกยอดขายรวม",
            "บันทึกยอดขายรวม",
            "กรอกสินค้าที่ขาย",
            "บันทึกสินค้าที่ขาย",
        ]:
            reply = handle_menu_message(normalized_message)

        # บันทึกยอดขาย เช่น ยอดขาย 2500
        elif normalized_message.startswith("ยอดขาย "):
            reply = handle_sales_message(user_message)

        # บันทึกสินค้าที่ขาย เช่น ขาย มัทฉะลาเต้ 2 110
        elif (
            normalized_message == "ขาย"
            or normalized_message.startswith("ขาย ")
        ):
            reply = handle_product_message(user_message)

        # บันทึกค่าใช้จ่าย
        elif (
            normalized_message == "ค่าใช้จ่าย"
            or normalized_message.startswith("ค่าใช้จ่าย ")
        ):
            reply = handle_expense_message(user_message)

        # บันทึกจำนวนลูกค้า
        elif (
            normalized_message == "ลูกค้า"
            or normalized_message.startswith("ลูกค้า ")
        ):
            reply = handle_customer_message(user_message)

        # รายงานประจำสัปดาห์
        elif normalized_message in [
            "รายงานสัปดาห์",
            "สรุปสัปดาห์",
        ]:
            reply = handle_weekly_report_message()

        # รายงานประจำเดือน
        elif normalized_message in [
            "รายงานเดือน",
            "สรุปเดือน",
        ]:
            reply = handle_monthly_report_message()

        # รายงานประจำวัน
        elif normalized_message in [
            "รายงาน",
            "สรุปวันนี้",
        ]:
            reply = handle_report_message()

        # ไม่พบคำสั่ง
        else:
            reply = (
                "ขออภัยค่ะ FlowMate ยังไม่เข้าใจข้อความนี้\n\n"
                "พิมพ์คำว่า “เมนู” เพื่อดูคำสั่งที่ใช้ได้"
            )

    except Exception as error:
        print(f"เกิดข้อผิดพลาดใน handlers.py: {error}")

        reply = (
            "⚠️ ระบบเกิดข้อผิดพลาดชั่วคราว\n\n"
            "กรุณาลองใหม่อีกครั้ง"
        )

    # ถ้าเป็นข้อความธรรมดา ให้สร้าง TextSendMessage
    if isinstance(reply, str):
        response_message = TextSendMessage(text=reply)

    # ถ้าเป็น FlexSendMessage ให้ส่งได้โดยตรง
    else:
        response_message = reply

    line_bot_api.reply_message(
        event.reply_token,
        response_message,
    )
