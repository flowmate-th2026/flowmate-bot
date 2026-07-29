from services import record_expense


def handle_expense_message(user_message):
    """
    ตรวจสอบและบันทึกข้อความค่าใช้จ่าย

    ตัวอย่าง:
    ค่าใช้จ่าย 350 ค่านม
    """

    normalized_message = user_message.lower().strip()

    if normalized_message == "ค่าใช้จ่าย":
        return (
            "💸 กรุณาใส่จำนวนเงินและรายละเอียด\n\n"
            "ตัวอย่าง:\n"
            "ค่าใช้จ่าย 350 ค่านม"
        )

    expense_text = user_message.replace("ค่าใช้จ่าย", "", 1).strip()
    expense_parts = expense_text.split(maxsplit=1)

    amount_text = expense_parts[0].replace(",", "")

    if len(expense_parts) > 1:
        description = expense_parts[1].strip()
    else:
        description = "ไม่ระบุรายละเอียด"

    try:
        amount = float(amount_text)

        if amount <= 0:
            return "❌ ค่าใช้จ่ายต้องมากกว่า 0 บาท"

        date_text, time_text = record_expense(
            amount,
            description,
        )

        if amount.is_integer():
            formatted_amount = f"{amount:,.0f}"
        else:
            formatted_amount = f"{amount:,.2f}"

        return (
            "✅ บันทึกค่าใช้จ่ายเรียบร้อย\n\n"
            f"📅 วันที่: {date_text}\n"
            f"⏰ เวลา: {time_text}\n"
            f"💸 ค่าใช้จ่าย: {formatted_amount} บาท\n"
            f"📝 รายละเอียด: {description}"
        )

    except ValueError:
        return (
            "❌ รูปแบบค่าใช้จ่ายไม่ถูกต้อง\n\n"
            "กรุณาพิมพ์ตัวเลข เช่น:\n"
            "ค่าใช้จ่าย 350 ค่านม"
        )

    except Exception as error:
        print(f"เกิดข้อผิดพลาดใน expense_handler.py: {error}")

        return (
            "⚠️ ระบบยังบันทึกค่าใช้จ่ายไม่ได้ในขณะนี้\n\n"
            "กรุณาลองใหม่อีกครั้ง"
        )
