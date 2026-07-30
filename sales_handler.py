from services import record_sale
from success_flex import create_success_flex


def handle_sales_message(
    user_message,
    sheet_id=None,
):
    """
    ตรวจสอบและบันทึกข้อความยอดขาย

    ตัวอย่าง:
    ยอดขาย 2500
    """

    normalized_message = user_message.lower().strip()

    if normalized_message == "ยอดขาย":
        return (
            "💰 กรุณาใส่จำนวนเงินต่อท้ายคำว่ายอดขาย\n\n"
            "ตัวอย่าง:\n"
            "ยอดขาย 2500"
        )

    amount_text = user_message.replace("ยอดขาย", "", 1).strip()
    amount_text = amount_text.replace(",", "")

    try:
        amount = float(amount_text)

        if amount <= 0:
            return "❌ ยอดขายต้องมากกว่า 0 บาท"

        date_text, time_text = record_sale(
            amount,
            sheet_id=sheet_id,
        )

        if amount.is_integer():
            formatted_amount = f"{amount:,.0f}"
        else:
            formatted_amount = f"{amount:,.2f}"

        return create_success_flex(
            record_type="ยอดขาย",
            amount=amount,
            description=f"ยอดขาย {formatted_amount} บาท",
            date_text=date_text,
            time_text=time_text,
            category="ยอดขาย",
        )

    except ValueError:
        return (
            "❌ รูปแบบยอดขายไม่ถูกต้อง\n\n"
            "กรุณาพิมพ์ตัวเลข เช่น:\n"
            "ยอดขาย 2500"
        )

    except Exception as error:
        print(f"เกิดข้อผิดพลาดใน sales_handler.py: {error}")

        return (
            "⚠️ ระบบยังบันทึกยอดขายไม่ได้ในขณะนี้\n\n"
            "กรุณาลองใหม่อีกครั้ง"
        )
