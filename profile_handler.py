from sheet_service import update_shop_profile

def handle_update_shop_profile_message(
    user_message,
    line_user_id,
):
    """
    แก้ไขข้อมูลโปรไฟล์ร้าน

    ตัวอย่าง:
    แก้ชื่อร้าน ครัวป้าหนุ่ย
    แก้ประเภทธุรกิจ ร้านอาหารตามสั่ง
    แก้จังหวัด ลำพูน
    แก้ผู้ติดต่อ ป้าหนุ่ย
    """

    command_fields = {
        "แก้ชื่อร้าน": (
            "shop_name",
            "ชื่อร้าน",
        ),
        "แก้ประเภทธุรกิจ": (
            "business_type",
            "ประเภทธุรกิจ",
        ),
        "แก้จังหวัด": (
            "province",
            "จังหวัด",
        ),
        "แก้ผู้ติดต่อ": (
            "contact_name",
            "ผู้ติดต่อ",
        ),
    }

    selected_command = None
    selected_field = None
    field_label = None

    for command, field_data in command_fields.items():
        if (
            user_message == command
            or user_message.startswith(command + " ")
        ):
            selected_command = command
            selected_field = field_data[0]
            field_label = field_data[1]
            break

    if not selected_command:
        return (
            "❌ ไม่พบคำสั่งแก้ไขโปรไฟล์\n\n"
            "ตัวอย่าง:\n"
            "แก้ชื่อร้าน ครัวป้าหนุ่ย\n"
            "แก้จังหวัด ลำพูน"
        )

    new_value = user_message.replace(
        selected_command,
        "",
        1,
    ).strip()

    if not new_value:
        return (
            f"✏️ กรุณาใส่{field_label}ใหม่\n\n"
            f"ตัวอย่าง:\n{selected_command} ข้อมูลใหม่"
        )

    if len(new_value) > 100:
        return (
            f"❌ {field_label}ยาวเกินไปค่ะ\n\n"
            "กรุณาใช้ข้อความไม่เกิน 100 ตัวอักษร"
        )

    result = update_shop_profile(
        line_user_id=line_user_id,
        field_name=selected_field,
        new_value=new_value,
    )

    if result["success"]:
        return (
            "✅ แก้ไขโปรไฟล์ร้านเรียบร้อยแล้ว\n\n"
            f"{field_label}: {result['new_value']}\n\n"
            "พิมพ์ “โปรไฟล์ร้าน” เพื่อตรวจสอบข้อมูล"
        )

    if result.get("reason") == "shop_not_found":
        return (
            "❌ ยังไม่พบข้อมูลร้านของคุณในระบบ\n\n"
            "กรุณาลงทะเบียนร้านก่อน"
        )

    return (
        "⚠️ ระบบยังแก้ไขโปรไฟล์ไม่ได้ในขณะนี้\n\n"
        "กรุณาลองใหม่อีกครั้ง"
    )

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
