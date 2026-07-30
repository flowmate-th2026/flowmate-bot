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
        
from collections import defaultdict

from sheet_service import get_product_rows_by_date
from services import get_thailand_time

def get_top_products_data(date_text, limit=3):
    """
    คืนข้อมูลสินค้าขายดีตามวันที่

    ตัวอย่างผลลัพธ์:
    [
        {
            "name": "ชาไทย",
            "quantity": 5,
            "amount": 250.0,
        }
    ]
    """

    product_rows = get_product_rows_by_date(date_text)

    product_summary = defaultdict(
        lambda: {
            "quantity": 0,
            "amount": 0.0,
        }
    )

    for row in product_rows:
        product_name = str(
            row.get("ชื่อสินค้า", "")
        ).strip()

        try:
            quantity = int(
                float(row.get("จำนวนขาย", 0) or 0)
            )
        except (ValueError, TypeError):
            quantity = 0

        try:
            amount = float(
                row.get("จำนวนเงิน", 0) or 0
            )
        except (ValueError, TypeError):
            amount = 0.0

        if product_name:
            product_summary[product_name]["quantity"] += quantity
            product_summary[product_name]["amount"] += amount

    sorted_products = sorted(
        product_summary.items(),
        key=lambda item: (
            item[1]["quantity"],
            item[1]["amount"],
        ),
        reverse=True,
    )

    top_products = []

    for product_name, data in sorted_products[:limit]:
        top_products.append(
            {
                "name": product_name,
                "quantity": data["quantity"],
                "amount": data["amount"],
            }
        )

    return top_products

def handle_top_products_message():
    """
    สรุปสินค้าขายดี Top 3 ของวันนี้
    """

    now = get_thailand_time()
    date_text = now.strftime("%d/%m/%Y")

    product_rows = get_product_rows_by_date(date_text)
    top_products = get_top_products_data(date_text, limit=3)

    if not top_products:
        return (
            "🏆 สินค้าขายดีวันนี้\n\n"
            "ยังไม่มีข้อมูลการขายสินค้าในวันนี้ค่ะ"
        )

    medals = ["🥇", "🥈", "🥉"]

    report_lines = [
        "🏆 สินค้าขายดีวันนี้",
        "",
    ]

    for index, product in enumerate(top_products):
        report_lines.append(
            f"{medals[index]} {product['name']}"
        )
        report_lines.append(
            f"   {product['quantity']} ชิ้น"
            f" — {product['amount']:,.2f} บาท"
        )

    total_quantity = 0
    total_amount = 0.0

    for row in product_rows:
        try:
            quantity = int(
                float(row.get("จำนวนขาย", 0) or 0)
            )
        except (ValueError, TypeError):
            quantity = 0

        try:
            amount = float(
                row.get("จำนวนเงิน", 0) or 0
            )
        except (ValueError, TypeError):
            amount = 0.0

        total_quantity += quantity
        total_amount += amount

    report_lines.extend(
        [
            "",
            f"รวมขายสินค้า {total_quantity} ชิ้น",
            f"ยอดขายสินค้า {total_amount:,.2f} บาท",
        ]
    )

    return "\n".join(report_lines)
