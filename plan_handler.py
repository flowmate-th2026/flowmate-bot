from datetime import datetime

from plan_service import (
    FEATURE_LABELS,
    PLAN_FEATURES,
    normalize_plan_name,
)
from services import get_thailand_time


def handle_plan_status_message(shop):
    """
    แสดงข้อมูลแพ็กเกจปัจจุบันของร้าน
    """

    if not shop:
        return (
            "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
            "พิมพ์ “ลงทะเบียนร้าน ชื่อร้าน” เพื่อส่งคำขอ"
        )

    shop_name = str(
        shop.get("shop_name", "-")
    ).strip()

    shop_status = str(
        shop.get("status", "")
    ).strip().lower()

    plan_name = normalize_plan_name(
        shop.get("plan_name", "")
    )

    end_date_text = str(
        shop.get("trial_end", "")
    ).strip()

    if shop_status == "pending":
        return (
            "⏳ ร้านของคุณกำลังรอตรวจสอบ\n\n"
            f"ชื่อร้าน: {shop_name}"
        )

    if shop_status == "inactive":
        return (
            "⛔ ร้านนี้ถูกระงับการใช้งานชั่วคราว\n\n"
            "กรุณาติดต่อผู้ดูแล RooYod"
        )

    if not plan_name:
        return (
            "⚠️ ร้านนี้ยังไม่ได้กำหนดแพ็กเกจ\n\n"
            "กรุณาติดต่อผู้ดูแล RooYod"
        )

    if plan_name not in PLAN_FEATURES:
        return (
            "⚠️ ข้อมูลแพ็กเกจของร้านไม่ถูกต้อง\n\n"
            f"แพ็กเกจปัจจุบัน: {plan_name}\n\n"
            "กรุณาติดต่อผู้ดูแล RooYod"
        )

    display_plan = {
        "trial": "Trial",
        "basic": "Basic",
        "pro": "Pro",
    }.get(
        plan_name,
        plan_name.title(),
    )

    status_text = "ใช้งานได้"
    days_text = "-"
    expiry_text = end_date_text or "-"

    if end_date_text:
        try:
            end_date = datetime.strptime(
                end_date_text,
                "%d/%m/%Y",
            ).date()

            today = get_thailand_time().date()
            days_left = (end_date - today).days

            warning_text = ""

            if days_left < 0:
                status_text = "หมดอายุแล้ว"
                days_text = "0 วัน"

            elif days_left == 0:
                status_text = "วันสุดท้าย"
                days_text = "เหลือวันนี้เป็นวันสุดท้าย"
                warning_text = (
                    "🚨 วันนี้เป็นวันสุดท้ายของแพ็กเกจ\n"
                    "กรุณาต่ออายุภายในวันนี้เพื่อใช้งาน RooYod ต่อเนื่อง"
                )

            elif days_left == 1:
                status_text = "ใกล้หมดอายุ"
                days_text = "เหลือ 1 วัน"
                warning_text = (
                    "🚨 แพ็กเกจของคุณจะหมดอายุพรุ่งนี้\n"
                    "แนะนำให้ต่ออายุก่อนสิทธิ์ถูกระงับ"
                )

            elif days_left <= 3:
                status_text = "ใกล้หมดอายุ"
                days_text = f"{days_left} วัน"
                warning_text = (
                    f"⚠️ แพ็กเกจของคุณจะหมดอายุในอีก {days_left} วัน\n"
                    "แนะนำให้ต่ออายุล่วงหน้า"
                )

            elif days_left <= 7:
                status_text = "ใกล้หมดอายุ"
                days_text = f"{days_left} วัน"
                warning_text = (
                    f"🔔 แพ็กเกจของคุณจะหมดอายุในอีก {days_left} วัน"
                )

            else:
                status_text = "ใช้งานได้"
                days_text = f"{days_left} วัน"

        except ValueError:
            return (
                "⚠️ รูปแบบวันหมดอายุไม่ถูกต้อง\n\n"
                "กรุณาติดต่อผู้ดูแล RooYod"
            )

    if status_text in ["หมดอายุแล้ว", "หมดอายุวันนี้"]:
        allowed_features = set()
    else:
        allowed_features = PLAN_FEATURES.get(
            plan_name,
            set(),
        )

    feature_lines = []

    for feature_name, feature_label in FEATURE_LABELS.items():
        if feature_name in allowed_features:
            feature_lines.append(
                f"✅ {feature_label}"
            )

    features_text = "\n".join(
        feature_lines
    )

    if status_text in ["หมดอายุแล้ว", "หมดอายุวันนี้"]:
        feature_section = (
            "🔒 ฟีเจอร์ถูกระงับชั่วคราว\n"
            "กรุณาต่ออายุแพ็กเกจเพื่อใช้งานต่อ"
        )
    else:
        feature_section = (
            "ฟีเจอร์ที่ใช้ได้:\n"
            f"{features_text}"
        )

    warning_section = ""

    if warning_text:
        warning_section = (
            f"\n\n{warning_text}"
        )

    return (
        "💳 แพ็กเกจ RooYod\n\n"
        f"ร้าน: {shop_name}\n"
        f"แพ็กเกจ: {display_plan}\n"
        f"สถานะ: {status_text}\n"
        f"หมดอายุ: {expiry_text}\n"
        f"เหลืออีก: {days_text}"
        f"{warning_section}\n\n"
        f"{feature_section}"
    )