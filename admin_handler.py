from sheet_service import (
    activate_shop,
    get_pending_shops,
    renew_shop_plan,
    validate_shop_sheet,
)

def handle_renew_shop_message(user_message):
    """
    ต่ออายุสิทธิ์ใช้งานร้าน

    ตัวอย่าง:
    ต่ออายุ SHOP001 30 Basic
    """

    command_parts = user_message.split(maxsplit=3)

    if len(command_parts) < 4:
        return (
            "💳 รูปแบบคำสั่งต่ออายุไม่ถูกต้อง\n\n"
            "กรุณาพิมพ์:\n"
            "ต่ออายุ SHOP001 30 Basic"
        )

    shop_id = command_parts[1].strip()
    days = command_parts[2].strip()
    plan_name = command_parts[3].strip()

    result = renew_shop_plan(
        shop_id=shop_id,
        days=days,
        plan_name=plan_name,
    )

    if result["success"]:
        return (
            "✅ ต่ออายุร้านเรียบร้อยแล้ว\n\n"
            f"รหัสร้าน: {result['shop_id']}\n"
            f"ชื่อร้าน: {result['shop_name']}\n"
            f"แพ็กเกจ: {result['plan_name']}\n"
            f"เพิ่มวันใช้งาน: {result['days_added']} วัน\n"
            f"หมดอายุใหม่: {result['new_end_date']}\n"
            "สถานะ: active"
        )

    reason = result.get("reason", "")

    if reason == "shop_not_found":
        return (
            "❌ ไม่พบรหัสร้านนี้ในระบบ\n\n"
            f"รหัสที่ค้นหา: {result.get('shop_id', '-')}"
        )

    if reason == "invalid_days":
        return (
            "❌ จำนวนวันต่ออายุไม่ถูกต้อง\n\n"
            "กรุณาใส่จำนวนเต็มมากกว่า 0"
        )

    if reason == "invalid_plan_name":
        return (
            "❌ ชื่อแพ็กเกจไม่ถูกต้อง\n\n"
            "แพ็กเกจที่ใช้ได้:\n"
            "- Basic\n"
            "- Pro\n\n"
            "ตัวอย่าง:\n"
            "ต่ออายุ SHOP001 30 Basic"
        )

    if reason == "missing_plan_name":
        return (
            "❌ กรุณาระบุชื่อแพ็กเกจ"
        )

    return (
        "⚠️ ระบบยังต่ออายุร้านไม่ได้ในขณะนี้\n\n"
        "กรุณาตรวจข้อมูลแล้วลองอีกครั้ง"
    )
    
def handle_pending_shops_message():
    """
    แสดงรายการร้านที่รอเปิดใช้งาน
    """

    pending_shops = get_pending_shops()

    if not pending_shops:
        return (
            "✅ ไม่มีร้านที่รอเปิดใช้งานในขณะนี้"
        )

    report_lines = [
        "🏪 ร้านที่รอเปิดใช้งาน",
        "",
    ]

    for index, shop in enumerate(
        pending_shops,
        start=1,
    ):
        sheet_status = (
            "มี Sheet ID แล้ว"
            if shop.get("sheet_id")
            else "ยังไม่มี Sheet ID"
        )

        report_lines.extend(
            [
                f"{index}. {shop['shop_name']}",
                f"รหัสร้าน: {shop['shop_id']}",
                f"สถานะชีต: {sheet_status}",
                "",
            ]
        )

    report_lines.append(
        f"รวมทั้งหมด {len(pending_shops)} ร้าน"
    )

    return "\n".join(report_lines)

def handle_activate_shop_message(user_message):
    """
    เปิดใช้งานร้านใหม่

    ตัวอย่าง:
    เปิดร้าน SHOP004 SHEET_ID

    หรือในอนาคต:
    เปิดร้าน SHOP004
    """

    command_parts = user_message.split(maxsplit=2)

    if len(command_parts) < 2:
        return (
            "🏪 รูปแบบคำสั่งเปิดร้านไม่ถูกต้อง\n\n"
            "กรุณาพิมพ์:\n"
            "เปิดร้าน SHOP004 SHEET_ID"
        )

    shop_id = command_parts[1].strip()

    sheet_id = None

    if len(command_parts) >= 3:
        sheet_id = command_parts[2].strip()

    if sheet_id:
        sheet_check = validate_shop_sheet(sheet_id)

    if not sheet_check["success"]:
        reason = sheet_check.get("reason", "")

        if reason == "permission_denied":
            return (
                "❌ RooYod ยังไม่มีสิทธิ์เข้าถึง Google Sheet นี้\n\n"
                "กรุณาแชร์ Sheet ให้ Service Account "
                "ด้วยสิทธิ์ Editor แล้วลองใหม่"
            )

        if reason == "sheet_not_found":
            return (
                "❌ ไม่สามารถเข้าถึง Google Sheet นี้ได้\n\n"
                "กรุณาตรวจสอบว่า:\n"
                "1. Sheet ID ถูกต้อง\n"
                "2. แชร์ Sheet ให้ Service Account แล้ว\n"
                "3. ให้สิทธิ์ Service Account เป็น Editor"
            )

        if reason == "worksheet_not_found":
            return (
                "❌ Google Sheet นี้ไม่มี Worksheet สำหรับใช้งาน"
            )

        return (
            "⚠️ RooYod ยังไม่สามารถเข้าถึง Google Sheet นี้ได้\n\n"
            "กรุณาตรวจสอบ Sheet ID และแชร์ Sheet ให้ "
            "Service Account ด้วยสิทธิ์ Editor แล้วลองใหม่"
        )

    result = activate_shop(
        shop_id=shop_id,
        sheet_id=sheet_id,
    )

    if result["success"]:
        reason = result.get("reason", "")

        if reason == "already_active":
            return (
                "✅ ร้านนี้เปิดใช้งานอยู่แล้ว\n\n"
                f"รหัสร้าน: {result['shop_id']}\n"
                f"ชื่อร้าน: {result['shop_name']}\n"
                "สถานะ: active"
            )

        return (
            "✅ เปิดใช้งานร้านเรียบร้อยแล้ว\n\n"
            f"รหัสร้าน: {result['shop_id']}\n"
            f"ชื่อร้าน: {result['shop_name']}\n"
            f"แพ็กเกจ: {result.get('plan_name', 'trial')}\n"
            f"เริ่มทดลอง: {result.get('trial_start', '-')}\n"
            f"หมดอายุ: {result.get('trial_end', '-')}\n"
            "สถานะ: active\n\n"
            "ร้านสามารถเริ่มใช้งาน RooYod ได้แล้วค่ะ"
        )

    reason = result.get("reason", "")

    if reason == "shop_not_found":
        return (
            "❌ ไม่พบรหัสร้านนี้ในระบบ\n\n"
            f"รหัสที่ค้นหา: {result.get('shop_id', '-')}"
        )

    if reason == "missing_shop_name":
        return (
            "❌ ร้านนี้ยังไม่มีชื่อร้านในระบบ\n\n"
            f"รหัสร้าน: {result.get('shop_id', '-')}\n"
            "กรุณาเพิ่มชื่อร้านใน Shop Registry ก่อนเปิดใช้งาน"
        )

    return (
        "⚠️ ระบบยังเปิดใช้งานร้านไม่ได้ในขณะนี้\n\n"
        "กรุณาตรวจรหัสร้านแล้วลองอีกครั้ง"
    )