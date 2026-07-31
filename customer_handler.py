from services import record_customer


def handle_customer_message(
    user_message,
    sheet_id=None,
):
    """
    ตรวจสอบและบันทึกจำนวนลูกค้า

    ตัวอย่าง:
    ลูกค้า 5
    """

    normalized_message = user_message.lower().strip()

    if normalized_message == "ลูกค้า":
        return (
            "👥 กรุณาใส่จำนวนลูกค้า\n\n"
            "ตัวอย่าง:\n"
            "ลูกค้า 5"
        )

    customer_text = user_message.replace("ลูกค้า", "", 1).strip()
    customer_text = customer_text.replace(",", "")

    try:
        customer_count = int(customer_text)

        if customer_count <= 0:
            return "❌ จำนวนลูกค้าต้องมากกว่า 0 คน"

        date_text, time_text = record_customer(
            customer_count=customer_count,
            sheet_id=sheet_id,
        )

        return (
            "✅ บันทึกจำนวนลูกค้าเรียบร้อย\n\n"
            f"📅 วันที่: {date_text}\n"
            f"⏰ เวลา: {time_text}\n"
            f"👥 จำนวนลูกค้า: {customer_count:,} คน"
        )

    except ValueError:
        return (
            "❌ รูปแบบจำนวนลูกค้าไม่ถูกต้อง\n\n"
            "กรุณาพิมพ์เป็นจำนวนเต็ม เช่น:\n"
            "ลูกค้า 5"
        )

    except Exception as error:
        print(f"เกิดข้อผิดพลาดใน customer_handler.py: {error}")

        return (
            "⚠️ ระบบยังบันทึกจำนวนลูกค้าไม่ได้ในขณะนี้\n\n"
            "กรุณาลองใหม่อีกครั้ง"
        )
