from sheet_service import activate_shop, get_pending_shops


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
    เปิดร้าน SHOP003 1AbCdEfGh...
    """

    command_parts = user_message.split(maxsplit=2)

    if len(command_parts) < 3:
        return (
            "🏪 รูปแบบคำสั่งเปิดร้านไม่ถูกต้อง\n\n"
            "กรุณาพิมพ์:\n"
            "เปิดร้าน SHOP003 SHEET_ID"
        )

    shop_id = command_parts[1].strip()
    sheet_id = command_parts[2].strip()

    result = activate_shop(
        shop_id=shop_id,
        sheet_id=sheet_id,
    )

    if result["success"]:
        return (
            "✅ เปิดใช้งานร้านเรียบร้อยแล้ว\n\n"
            f"รหัสร้าน: {result['shop_id']}\n"
            f"ชื่อร้าน: {result['shop_name']}\n"
            "สถานะ: active\n\n"
            "ร้านสามารถเริ่มใช้งาน RooYod ได้แล้วค่ะ"
        )

    reason = result.get("reason", "")

    if reason == "shop_not_found":
        return (
            "❌ ไม่พบรหัสร้านนี้ในระบบ\n\n"
            f"รหัสที่ค้นหา: {result.get('shop_id', '-')}"
        )

    if reason == "missing_sheet_id":
        return (
            "❌ กรุณาใส่ Sheet ID ของร้าน"
        )

    return (
        "⚠️ ระบบยังเปิดใช้งานร้านไม่ได้ในขณะนี้\n\n"
        "กรุณาตรวจรหัสร้านและ Sheet ID แล้วลองอีกครั้ง"
    )
