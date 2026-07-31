from linebot.models import TextSendMessage

from customer_handler import handle_customer_message
from expense_handler import handle_expense_message
from menu_handler import handle_menu_message
from period_report_handler import (
    handle_monthly_report_message,
    handle_weekly_report_message,
)
from product_handler import (
    handle_product_message,
    handle_top_products_message,
)
from report_handler import handle_report_message
from sales_handler import handle_sales_message
from sheet_service import get_shop_by_line_user_id


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

        elif normalized_message in [
            "ไอดีร้าน",
            "line id",
            "line user id",
        ]:
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            if shop:
                reply = (
                    "✅ พบข้อมูลร้านแล้ว\n\n"
                    f"รหัสร้าน: {shop['shop_id']}\n"
                    f"ชื่อร้าน: {shop['shop_name']}\n"
                    f"สถานะ: {shop['status']}"
                )
            else:
                reply = (
                    "❌ ยังไม่พบข้อมูลร้านนี้ในระบบ\n\n"
                    f"LINE User ID:\n{line_user_id}"
                )
        
        # บันทึกยอดขาย เช่น ยอดขาย 2500
        elif normalized_message.startswith("ยอดขาย "):
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            if not shop:
                reply = (
                    "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
                    "กรุณาติดต่อผู้ดูแล FlowMate"
                )
            else:
                reply = handle_sales_message(
                    user_message,
                    sheet_id=shop["sheet_id"],
                )

        # ดูสินค้าขายดี Top 3
        elif normalized_message in [
            "สินค้าขายดี",
            "ขายดี",
            "top 3",
            "top3",
        ]:
            reply = handle_top_products_message()
            
        # บันทึกสินค้าที่ขาย เช่น ขาย มัทฉะลาเต้ 2 110
        elif (
            normalized_message == "ขาย"
            or normalized_message.startswith("ขาย ")
        ):
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            if not shop:
                reply = (
                    "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
                    "กรุณาติดต่อผู้ดูแล FlowMate"
                )
            else:
                reply = handle_product_message(
                    user_message,
                    sheet_id=shop["sheet_id"],
                )

        # บันทึกค่าใช้จ่าย
        elif (
            normalized_message == "ค่าใช้จ่าย"
            or normalized_message.startswith("ค่าใช้จ่าย ")
        ):
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            if not shop:
                reply = (
                    "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
                    "กรุณาติดต่อผู้ดูแล FlowMate"
                )
            else:
                reply = handle_expense_message(
                    user_message,
                    sheet_id=shop["sheet_id"],
                )

        # บันทึกจำนวนลูกค้า
        elif (
            normalized_message == "ลูกค้า"
            or normalized_message.startswith("ลูกค้า ")
        ):
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            if not shop:
                reply = (
                    "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
                    "กรุณาติดต่อผู้ดูแล FlowMate"
                )
            else:
                reply = handle_customer_message(
                    user_message,
                    sheet_id=shop["sheet_id"],
                )

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
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            if not shop:
                reply = (
                    "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
                    "กรุณาติดต่อผู้ดูแล FlowMate"
                )
            else:
                reply = handle_report_message(
                    sheet_id=shop["sheet_id"],
                )

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
