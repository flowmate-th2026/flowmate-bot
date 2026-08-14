from curses import error

from sheet_service import register_shop_request
from linebot.models import TextSendMessage
from config import ADMIN_LINE_USER_ID

def handle_register_shop_message(
    user_message,
    line_user_id,
    line_bot_api,
):
    """
    รับคำสั่งลงทะเบียนร้าน

    ตัวอย่าง:
    ลงทะเบียนร้าน คาเฟ่บ้านสวน
    """

    shop_name = user_message.replace(
        "ลงทะเบียนร้าน",
        "",
        1,
    ).strip()

    if not shop_name:
        return (
            "🏪 กรุณาใส่ชื่อร้านต่อท้ายคำว่า "
            "ลงทะเบียนร้าน\n\n"
            "ตัวอย่าง:\n"
            "ลงทะเบียนร้าน คาเฟ่บ้านสวน"
        )

    if len(shop_name) > 100:
        return (
            "❌ ชื่อร้านยาวเกินไปค่ะ\n\n"
            "กรุณาใช้ชื่อร้านไม่เกิน 100 ตัวอักษร"
        )

    result = register_shop_request(
        line_user_id=line_user_id,
        shop_name=shop_name,
    )

    if result["success"]:
        admin_message = (
            "🔔 มีร้านใหม่ขอลงทะเบียน RooYod\n\n"
            f"รหัสร้าน: {result['shop_id']}\n"
            f"ชื่อร้าน: {result['shop_name']}\n"
            "สถานะ: pending\n\n"
            f"พิมพ์ “เปิดร้าน {result['shop_id']}” "
            "เพื่อตรวจสอบและเปิดใช้งาน"
        )

        try:
            if ADMIN_LINE_USER_ID:
                line_bot_api.push_message(
                ADMIN_LINE_USER_ID,
                TextSendMessage(text=admin_message),
            )
        except Exception as error:
            print(
                "ไม่สามารถส่งแจ้งเตือนร้านใหม่ให้ Admin:",
                error,
            )

        return (
            "✅ รับคำขอลงทะเบียนเรียบร้อยแล้ว\n\n"
            f"รหัสร้าน: {result['shop_id']}\n"
            f"ชื่อร้าน: {result['shop_name']}\n"
            "สถานะ: รอตรวจสอบ\n\n"
            "ผู้ดูแลจะเปิดใช้งานร้านให้ภายหลังค่ะ"
        )

    status = result.get("status", "")

    if status == "active":
        return (
            "✅ ร้านนี้เปิดใช้งานอยู่แล้ว\n\n"
            f"รหัสร้าน: {result['shop_id']}\n"
            f"ชื่อร้าน: {result['shop_name']}"
        )

    if status == "pending":
        return (
            "⏳ ร้านนี้ส่งคำขอลงทะเบียนแล้ว\n\n"
            f"รหัสร้าน: {result['shop_id']}\n"
            f"ชื่อร้าน: {result['shop_name']}\n"
            "สถานะ: รอตรวจสอบ"
        )

    return (
        "⚠️ LINE บัญชีนี้มีข้อมูลอยู่ในระบบแล้ว\n\n"
        "กรุณาติดต่อผู้ดูแล FlowMate"
    )
