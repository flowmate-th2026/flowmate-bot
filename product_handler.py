from services import record_product


def handle_product_message(user_message):
    """
    ตรวจสอบและบันทึกสินค้าที่ขาย

    รูปแบบ:
    ขาย ชื่อสินค้า จำนวน ยอดขายรวม

    ตัวอย่าง:
    ขาย มัทฉะลาเต้ 2 110
    """

    normalized_message = user_message.lower().strip()

    if normalized_message == "ขาย":
        return (
            "🛍️ กรุณาใส่ชื่อสินค้า จำนวน และยอดขายรวม\n\n"
            "ตัวอย่าง:\n"
            "ขาย มัทฉะลาเต้ 2 110"
        )

    product_text = user_message.replace("ขาย", "", 1).strip()

    # แบ่งข้อมูลจากด้านขวา 2 ตำแหน่ง
    # เพื่อรองรับชื่อสินค้าที่มีหลายคำ
    product_parts = product_text.rsplit(maxsplit=2)

    if len(product_parts) != 3:
        return (
            "❌ รูปแบบการบันทึกสินค้าไม่ถูกต้อง\n\n"
            "กรุณาพิมพ์ตามตัวอย่าง:\n"
            "ขาย มัทฉะลาเต้ 2 110"
        )

    product_name = product_parts[0].strip()
    quantity_text = product_parts[1].replace(",", "")
    amount_text = product_parts[2].replace(",", "")

    if not product_name:
        return "❌ กรุณาระบุชื่อสินค้า"

    try:
        quantity = int(quantity_text)
        amount = float(amount_text)

        if quantity <= 0:
            return "❌ จำนวนขายต้องมากกว่า 0 ชิ้น"

        if amount <= 0:
            return "❌ ยอดขายรวมต้องมากกว่า 0 บาท"

        date_text, time_text = record_product(
            product_name=product_name,
            quantity=quantity,
            amount=amount,
        )

        if amount.is_integer():
            formatted_amount = f"{amount:,.0f}"
        else:
            formatted_amount = f"{amount:,.2f}"

        return (
            "✅ บันทึกสินค้าที่ขายเรียบร้อย\n\n"
            f"📅 วันที่: {date_text}\n"
            f"⏰ เวลา: {time_text}\n"
            f"🛍️ สินค้า: {product_name}\n"
            f"🔢 จำนวน: {quantity:,} ชิ้น\n"
            f"💰 ยอดขายรวม: {formatted_amount} บาท"
        )

    except ValueError:
        return (
            "❌ จำนวนขายและยอดเงินต้องเป็นตัวเลข\n\n"
            "ตัวอย่าง:\n"
            "ขาย มัทฉะลาเต้ 2 110"
        )

    except Exception as error:
        print(f"เกิดข้อผิดพลาดใน product_handler.py: {error}")

        return (
            "⚠️ ระบบยังบันทึกสินค้าไม่ได้ในขณะนี้\n\n"
            "กรุณาลองใหม่อีกครั้ง"
        )
