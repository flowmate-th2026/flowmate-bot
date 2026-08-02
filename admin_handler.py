from sheet_service import get_pending_shops


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
