PLAN_FEATURES = {
    "trial": {
        "record_sales",
        "record_product",
        "record_expense",
        "record_customer",
        "daily_report",
        "shop_profile",
    },
    "basic": {
        "record_sales",
        "record_product",
        "record_expense",
        "record_customer",
        "daily_report",
        "weekly_report",
        "top_products",
        "shop_profile",
    },
    "pro": {
        "record_sales",
        "record_product",
        "record_expense",
        "record_customer",
        "daily_report",
        "weekly_report",
        "monthly_report",
        "top_products",
        "shop_profile",
    },
}


FEATURE_LABELS = {
    "record_sales": "บันทึกยอดขาย",
    "record_product": "บันทึกสินค้าที่ขาย",
    "record_expense": "บันทึกค่าใช้จ่าย",
    "record_customer": "บันทึกจำนวนลูกค้า",
    "daily_report": "รายงานประจำวัน",
    "weekly_report": "รายงานประจำสัปดาห์",
    "monthly_report": "รายงานประจำเดือน",
    "top_products": "สินค้าขายดี",
    "shop_profile": "โปรไฟล์ร้าน",
}


def normalize_plan_name(plan_name):
    """
    แปลงชื่อแพ็กเกจให้อยู่ในรูปแบบมาตรฐาน
    """

    return str(plan_name or "").strip().lower()


def can_use_feature(plan_name, feature_name):
    """
    ตรวจว่าแพ็กเกจสามารถใช้ฟีเจอร์ที่ระบุได้หรือไม่
    """

    normalized_plan = normalize_plan_name(plan_name)

    allowed_features = PLAN_FEATURES.get(
        normalized_plan,
        set(),
    )

    return feature_name in allowed_features


def get_feature_access_message(
    plan_name,
    feature_name,
):
    """
    คืน None เมื่อใช้ฟีเจอร์ได้
    หรือคืนข้อความแจ้งเตือนเมื่อแพ็กเกจไม่รองรับ
    """

    if can_use_feature(
        plan_name=plan_name,
        feature_name=feature_name,
    ):
        return None

    feature_label = FEATURE_LABELS.get(
        feature_name,
        "ฟีเจอร์นี้",
    )

    display_plan = str(plan_name or "-").strip()

    return (
        "🔒 แพ็กเกจปัจจุบันยังไม่รองรับฟีเจอร์นี้\n\n"
        f"ฟีเจอร์: {feature_label}\n"
        f"แพ็กเกจปัจจุบัน: {display_plan}\n\n"
        "กรุณาติดต่อผู้ดูแล RooYod "
        "เพื่ออัปเกรดแพ็กเกจ"
    )
