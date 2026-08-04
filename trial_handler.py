from datetime import datetime

from services import get_thailand_time


def handle_trial_status_message(shop):
    """
    แสดงสถานะและจำนวนวันทดลองใช้ที่เหลือ
    """

    if not shop:
        return (
            "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
            "พิมพ์ “ลงทะเบียนร้าน ชื่อร้าน” เพื่อส่งคำขอ"
        )

    shop_name = shop.get("shop_name", "-")
    shop_status = shop.get("status", "")
    trial_start_text = str(
        shop.get("trial_start", "")
    ).strip()
    trial_end_text = str(
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

    if not trial_end_text:
        return (
            "⚠️ ร้านนี้ยังไม่ได้กำหนดวันหมดอายุทดลองใช้\n\n"
            "กรุณาติดต่อผู้ดูแล RooYod"
        )

    try:
        trial_end = datetime.strptime(
            trial_end_text,
            "%d/%m/%Y",
        ).date()

        today = get_thailand_time().date()
        days_left = (trial_end - today).days

        if days_left < 0:
            status_text = "หมดอายุแล้ว"
            days_text = "0 วัน"
        elif days_left == 0:
            status_text = "หมดอายุวันนี้"
            days_text = "เหลือวันนี้เป็นวันสุดท้าย"
        else:
            status_text = "ใช้งานได้"
            days_text = f"{days_left} วัน"

        return (
            "🎁 สถานะทดลองใช้ RooYod\n\n"
            f"ชื่อร้าน: {shop_name}\n"
            f"เริ่มทดลอง: {trial_start_text or '-'}\n"
            f"หมดอายุ: {trial_end_text}\n"
            f"เหลืออีก: {days_text}\n"
            f"แพ็กเกจ: {shop.get('plan_name', '-') or '-'}\n"
            f"สถานะ: {status_text}"
        )

    except ValueError:
        return (
            "⚠️ รูปแบบวันที่ทดลองใช้ไม่ถูกต้อง\n\n"
            "กรุณาติดต่อผู้ดูแล RooYod"
        )
