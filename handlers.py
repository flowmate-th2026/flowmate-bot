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
from register_handler import handle_register_shop_message
from admin_handler import (
    handle_activate_shop_message,
    handle_pending_shops_message,
    handle_renew_shop_message,
)
from config import ADMIN_LINE_USER_ID
from datetime import datetime

from services import get_thailand_time
from trial_handler import handle_trial_status_message
from profile_handler import (
    handle_shop_profile_message,
    handle_update_shop_profile_message,
)
from plan_service import get_feature_access_message
from plan_handler import handle_plan_status_message


def get_shop_access_message(shop):
    """
    ตรวจสถานะร้านก่อนอนุญาตให้ใช้งานระบบ
    """

    if not shop:
        return (
            "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
            "พิมพ์ “ลงทะเบียนร้าน ชื่อร้าน” เพื่อส่งคำขอ"
        )

    status = shop.get("status", "")
    sheet_id = shop.get("sheet_id", "")

    if status == "pending":
        return (
            "⏳ ร้านของคุณกำลังรอตรวจสอบ\n\n"
            f"รหัสร้าน: {shop.get('shop_id', '-')}\n"
            f"ชื่อร้าน: {shop.get('shop_name', '-')}\n\n"
            "ผู้ดูแลจะเปิดใช้งานให้ภายหลังค่ะ"
        )

    if status == "inactive":
        return (
            "⛔ ร้านนี้ถูกระงับการใช้งานชั่วคราว\n\n"
            "กรุณาติดต่อผู้ดูแล FlowMate"
        )

    if status != "active":
        return (
            "⚠️ สถานะร้านไม่ถูกต้อง\n\n"
            "กรุณาติดต่อผู้ดูแล FlowMate"
        )

    if not sheet_id:
        return (
            "⚠️ ร้านเปิดใช้งานแล้ว แต่ยังไม่ได้เชื่อม Google Sheets\n\n"
            "กรุณาติดต่อผู้ดูแล FlowMate"
        )

    trial_end_text = str(
        shop.get("trial_end", "")
    ).strip()

    if trial_end_text:
        try:
            trial_end = datetime.strptime(
                trial_end_text,
                "%d/%m/%Y",
            ).date()

            today = get_thailand_time().date()

            if today > trial_end:
                plan_name = str(
                    shop.get("plan_name", "")
                ).strip().lower()

                if plan_name == "trial":
                    expiry_title = (
                        "⏰ ระยะเวลาทดลองใช้ของร้านหมดแล้ว"
                    )
                elif plan_name == "basic":
                    expiry_title = (
                        "⏰ สิทธิ์ใช้งานแพ็กเกจ Basic หมดอายุแล้ว"
                    )
                elif plan_name == "pro":
                    expiry_title = (
                        "⏰ สิทธิ์ใช้งานแพ็กเกจ Pro หมดอายุแล้ว"
                    )
                else:
                    expiry_title = (
                        "⏰ สิทธิ์ใช้งาน RooYod หมดอายุแล้ว"
                    )

                return (
                    f"{expiry_title}\n\n"
                    f"หมดอายุวันที่: {trial_end_text}\n\n"
                    "กรุณาติดต่อผู้ดูแล RooYod "
                    "เพื่อต่ออายุการใช้งาน"
                )

        except ValueError:
            return (
                "⚠️ รูปแบบวันหมดอายุของร้านไม่ถูกต้อง\n\n"
                "กรุณาติดต่อผู้ดูแล RooYod"
            )
    return None


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

        elif normalized_message == "ทดสอบแจ้งเตือนร้านใหม่":
            line_user_id = event.source.user_id

            if line_user_id != ADMIN_LINE_USER_ID:
                reply = "⛔ คำสั่งนี้ใช้ได้เฉพาะผู้ดูแลระบบ"
            else:
                test_message = (
                    "🔔 มีร้านใหม่ขอลงทะเบียน RooYod\n\n"
                    "รหัสร้าน: SHOPTEST\n"
                    "ชื่อร้าน: ร้านทดสอบ Day34\n"
                    "สถานะ: pending\n\n"
                    "นี่คือข้อความทดสอบระบบแจ้งเตือน Admin"
                )

                line_bot_api.push_message(
                    ADMIN_LINE_USER_ID,
                    TextSendMessage(text=test_message),
                )

                reply = "✅ ส่งข้อความทดสอบแจ้งเตือน Admin แล้ว"

        elif normalized_message in [
            "ร้านรอเปิดใช้งาน",
            "ร้าน pending",
            "pending shops",
        ]:
            line_user_id = event.source.user_id

            if line_user_id != ADMIN_LINE_USER_ID:
                reply = (
                    "⛔ คำสั่งนี้ใช้ได้เฉพาะผู้ดูแลระบบ"
                )
            else:
                reply = handle_pending_shops_message()

        elif (
            normalized_message == "เปิดร้าน"
            or normalized_message.startswith("เปิดร้าน ")
        ):
            line_user_id = event.source.user_id

            if line_user_id != ADMIN_LINE_USER_ID:
                reply = (
                    "⛔ คำสั่งนี้ใช้ได้เฉพาะผู้ดูแลระบบ"
                )
            else:
                reply = handle_activate_shop_message(
                    user_message
                )
        elif (
            normalized_message == "ต่ออายุ"
            or normalized_message.startswith("ต่ออายุ ")
        ):
            line_user_id = event.source.user_id

            if line_user_id != ADMIN_LINE_USER_ID:
                reply = (
                    "⛔ คำสั่งนี้ใช้ได้เฉพาะผู้ดูแลระบบ"
                )
            else:
                reply = handle_renew_shop_message(
                    user_message
                )

        elif normalized_message in [
            "แพ็กเกจ",
            "แพ็กเกจของฉัน",
            "package",
        ]:
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            reply = handle_plan_status_message(shop)       
        
        elif (
            normalized_message == "ลงทะเบียนร้าน"
            or normalized_message.startswith("ลงทะเบียนร้าน ")
        ):
            line_user_id = event.source.user_id

            reply = handle_register_shop_message(
                user_message=user_message,
                line_user_id=line_user_id,
                line_bot_api=line_bot_api,
            )

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
                    "❌ ยังไม่พบข้อมูลร้านนี้ในระบบ"
                )

        elif normalized_message in [
            "โปรไฟล์ร้าน",
            "ข้อมูลร้าน",
            "shop profile",
        ]:
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            reply = handle_shop_profile_message(shop)

        elif (
            normalized_message == "แก้ชื่อร้าน"
            or normalized_message.startswith("แก้ชื่อร้าน ")
            or normalized_message == "แก้ประเภทธุรกิจ"
            or normalized_message.startswith("แก้ประเภทธุรกิจ ")
            or normalized_message == "แก้จังหวัด"
            or normalized_message.startswith("แก้จังหวัด ")
            or normalized_message == "แก้ผู้ติดต่อ"
            or normalized_message.startswith("แก้ผู้ติดต่อ ")
        ):
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
            else:
                reply = handle_update_shop_profile_message(
                    user_message=user_message,
                    line_user_id=line_user_id,
                )

        
        elif normalized_message in [
            "สถานะทดลองใช้",
            "ทดลองใช้",
            "trial status",
        ]:
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)

            reply = handle_trial_status_message(shop)
        
        # บันทึกยอดขาย เช่น ยอดขาย 2500
        elif normalized_message.startswith("ยอดขาย "):
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
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
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
            else:
                feature_message = get_feature_access_message(
                    plan_name=shop.get("plan_name", ""),
                    feature_name="top_products",
                )

                if feature_message:
                    reply = feature_message
                else:
                    reply = handle_top_products_message(
                        sheet_id=shop["sheet_id"],
                    )
            
        # บันทึกสินค้าที่ขาย เช่น ขาย มัทฉะลาเต้ 2 110
        elif (
            normalized_message == "ขาย"
            or normalized_message.startswith("ขาย ")
        ):
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
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
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
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
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
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
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
            else:
                feature_message = get_feature_access_message(
                    plan_name=shop.get("plan_name", ""),
                    feature_name="weekly_report",
                )

                if feature_message:
                    reply = feature_message
                else:
                    reply = handle_weekly_report_message(
                        sheet_id=shop["sheet_id"],
                    )

        # รายงานประจำเดือน
        elif normalized_message in [
            "รายงานเดือน",
            "สรุปเดือน",
        ]:
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
            else:
                feature_message = get_feature_access_message(
                    plan_name=shop.get("plan_name", ""),
                    feature_name="monthly_report",
                )

                if feature_message:
                    reply = feature_message
                else:
                    reply = handle_monthly_report_message(
                        sheet_id=shop["sheet_id"],
                    )

        # รายงานประจำวัน
        elif normalized_message in [
            "รายงาน",
            "สรุปวันนี้",
        ]:
            line_user_id = event.source.user_id
            shop = get_shop_by_line_user_id(line_user_id)
            access_message = get_shop_access_message(shop)

            if access_message:
                reply = access_message
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
        print(
            f"เกิดข้อผิดพลาดใน handlers.py: {repr(error)}",
            flush=True,
        )

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
