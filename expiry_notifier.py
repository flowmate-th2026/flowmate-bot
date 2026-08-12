from datetime import datetime

from services import get_thailand_time
from plan_service import normalize_plan_name
from sheet_service import (
    get_all_shops,
    update_last_expiry_notice,
)
from linebot.models import TextSendMessage

def get_expiry_notification(shop):
    """
    ตรวจว่าร้านควรได้รับข้อความแจ้งเตือนแพ็กเกจหรือไม่

    คืนค่า:
    - ข้อความแจ้งเตือน ถ้าควรแจ้ง
    - None ถ้ายังไม่ถึงวันที่ต้องแจ้ง
    """

    if not shop:
        return None

    status = str(
        shop.get("status", "")
    ).strip().lower()

    if status != "active":
        return None

    line_user_id = str(
        shop.get("line_user_id", "")
    ).strip()

    if not line_user_id:
        return None

    shop_name = str(
        shop.get("shop_name", "-")
    ).strip()

    plan_name = normalize_plan_name(
        shop.get("plan_name", "")
    )

    end_date_text = str(
        shop.get("trial_end", "")
    ).strip()

    if not end_date_text:
        return None

    try:
        end_date = datetime.strptime(
            end_date_text,
            "%d/%m/%Y",
        ).date()
    except ValueError:
        return None

    today = get_thailand_time().date()
    days_left = (end_date - today).days

    display_plan = {
        "trial": "Trial",
        "basic": "Basic",
        "pro": "Pro",
    }.get(
        plan_name,
        plan_name.title(),
    )

    if days_left == 7:
        return (
            f"🔔 แจ้งเตือนแพ็กเกจ RooYod\n\n"
            f"ร้าน: {shop_name}\n"
            f"แพ็กเกจ: {display_plan}\n"
            f"เหลืออีก: 7 วัน\n"
            f"หมดอายุ: {end_date_text}\n\n"
            "กรุณาต่ออายุล่วงหน้าเพื่อใช้งาน RooYod ได้อย่างต่อเนื่อง"
        )

    if days_left == 3:
        return (
            f"⚠️ แพ็กเกจใกล้หมดอายุ\n\n"
            f"ร้าน: {shop_name}\n"
            f"แพ็กเกจ: {display_plan}\n"
            f"เหลืออีก: 3 วัน\n"
            f"หมดอายุ: {end_date_text}\n\n"
            "แนะนำให้ต่ออายุล่วงหน้าค่ะ"
        )

    if days_left == 1:
        return (
            f"🚨 แพ็กเกจจะหมดอายุพรุ่งนี้\n\n"
            f"ร้าน: {shop_name}\n"
            f"แพ็กเกจ: {display_plan}\n"
            f"หมดอายุ: {end_date_text}\n\n"
            "กรุณาต่ออายุก่อนสิทธิ์ถูกระงับ"
        )

    if days_left == 0:
        return (
            f"⏰ แพ็กเกจหมดอายุวันนี้\n\n"
            f"ร้าน: {shop_name}\n"
            f"แพ็กเกจ: {display_plan}\n"
            f"หมดอายุ: {end_date_text}\n\n"
            "กรุณาต่ออายุเพื่อใช้งาน RooYod ต่อ"
        )

    return None

def get_all_expiry_notifications():
    """
    ตรวจร้านทั้งหมดใน Shop Registry
    และคืนเฉพาะร้านที่ต้องแจ้งเตือนวันนี้
    """

    shops = get_all_shops()
    notifications = []

    for shop in shops:
        message = get_expiry_notification(shop)

        if not message:
            continue

        line_user_id = str(
            shop.get("line_user_id", "")
        ).strip()

        trial_end_text = str(
            shop.get("trial_end", "")
        ).strip()

        trial_end = datetime.strptime(
            trial_end_text,
            "%d/%m/%Y",
        ).date()

        today = get_thailand_time().date()
        days_left = (trial_end - today).days    

        notifications.append(
            {
                "shop_id": shop.get("shop_id", ""),
                "shop_name": shop.get("shop_name", ""),
                "line_user_id": line_user_id,
                "message": message,
                "notice_value": f"{trial_end_text}|{days_left}",
                "last_expiry_notice": str(
                    shop.get("last_expiry_notice", "")
                ).strip(),
            }
        )

    return notifications

def send_expiry_notifications(line_bot_api):
    """
    ส่งแจ้งเตือนแพ็กเกจใกล้หมดอายุไปยัง LINE ของร้านค้า
    """

    notifications = get_all_expiry_notifications()
    results = []

    for item in notifications:
        line_user_id = str(
            item.get("line_user_id", "")
        ).strip()

        message = str(
            item.get("message", "")
        ).strip()

        notice_value = str(
            item.get("notice_value", "")
        ).strip()

        last_expiry_notice = str(
            item.get("last_expiry_notice", "")
        ).strip()

        shop_id = str(
            item.get("shop_id", "")
        ).strip()

        shop_name = str(
            item.get("shop_name", "")
        ).strip()

        if not line_user_id or not message:
            results.append(
                {
                    "shop_id": shop_id,
                    "shop_name": shop_name,
                    "success": False,
                    "reason": "missing_line_user_id_or_message",
                }
            )
            continue

        # เคยแจ้งรอบนี้แล้ว ไม่ต้องส่งซ้ำ
        if notice_value == last_expiry_notice:
            results.append(
                {
                    "shop_id": shop_id,
                    "shop_name": shop_name,
                    "success": True,
                    "skipped": True,
                    "reason": "already_notified",
                }
            )
            continue

        try:
            line_bot_api.push_message(
                line_user_id,
                TextSendMessage(text=message),
            )

            # บันทึกหลังส่ง LINE สำเร็จเท่านั้น
            update_last_expiry_notice(
                shop_id,
                notice_value,
            )

            results.append(
                {
                    "shop_id": shop_id,
                    "shop_name": shop_name,
                    "success": True,
                    "skipped": False,
                }
            )

        except Exception as error:
            results.append(
                {
                    "shop_id": shop_id,
                    "shop_name": shop_name,
                    "success": False,
                    "reason": str(error),
                }
            )

    return results


def send_test_expiry_notification(line_bot_api, target_shop_id):
    """
    ส่งแจ้งเตือนทดสอบเฉพาะร้านที่ระบุ
    """

    notifications = get_all_expiry_notifications()

    target_shop_id = str(
        target_shop_id
    ).strip()

    for item in notifications:
        shop_id = str(
            item.get("shop_id", "")
        ).strip()

        if shop_id != target_shop_id:
            continue

        line_user_id = str(
            item.get("line_user_id", "")
        ).strip()

        message = str(
            item.get("message", "")
        ).strip()

        notice_value = str(
            item.get("notice_value", "")
        ).strip()

        last_expiry_notice = str(
            item.get("last_expiry_notice", "")
        ).strip()

        if not line_user_id or not message:
            return {
                "success": False,
                "shop_id": shop_id,
                "reason": "missing_line_user_id_or_message",
            }

        # เคยแจ้งรอบนี้แล้ว
        if notice_value == last_expiry_notice:
            return {
                "success": True,
                "shop_id": shop_id,
                "skipped": True,
                "reason": "already_notified",
            }

        try:
            line_bot_api.push_message(
                line_user_id,
                TextSendMessage(text=message),
            )

            # ส่งสำเร็จแล้วค่อยบันทึก
            update_last_expiry_notice(
                shop_id,
                notice_value,
            )

            return {
                "success": True,
                "shop_id": shop_id,
                "skipped": False,
            }

        except Exception as error:
            return {
                "success": False,
                "shop_id": shop_id,
                "reason": str(error),
            }

    return {
        "success": False,
        "reason": "shop_not_in_notification_list",
    }