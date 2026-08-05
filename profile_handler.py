def handle_shop_profile_message(shop):
    """
    แสดงข้อมูลโปรไฟล์ร้าน
    """

    if not shop:
        return (
            "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
            "พิมพ์ “ลงทะเบียนร้าน ชื่อร้าน” เพื่อส่งคำขอ"
        )

    shop_name = shop.get("shop_name", "") or "-"
    shop_id = shop.get("shop_id", "") or "-"
    business_type = shop.get("business_type", "") or "-"
    province = shop.get("province", "") or "-"
    contact_name = shop.get("contact_name", "") or "-"
    plan_name = shop.get("plan_name", "") or "-"
    status = shop.get("status", "") or "-"

    return (
        "🏪 โปรไฟล์ร้าน RooYod\n\n"
        f"รหัสร้าน: {shop_id}\n"
        f"ชื่อร้าน: {shop_name}\n"
        f"ประเภทธุรกิจ: {business_type}\n"
        f"จังหวัด: {province}\n"
        f"ผู้ติดต่อ: {contact_name}\n"
        f"แพ็กเกจ: {plan_name}\n"
        f"สถานะ: {status}"
    )
