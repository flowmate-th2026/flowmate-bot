from linebot.models import FlexSendMessage
from menu_flex import create_main_menu_flex

def create_sales_flex_message():
    return FlexSendMessage(
        alt_text="เมนูยอดขาย FlowMate",
        contents={
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#FFF1D6",
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "text",
                        "text": "💰 เมนูยอดขาย",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#A84B00",
                    },
                    {
                        "type": "text",
                        "text": "เลือกสิ่งที่ต้องการทำ",
                        "size": "sm",
                        "color": "#8B6B4A",
                        "margin": "sm",
                    },
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#F59E0B",
                        "action": {
                            "type": "message",
                            "label": "บันทึกยอดขายรวม",
                            "text": "กรอกยอดขายรวม",
                        },
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "บันทึกสินค้าที่ขาย",
                            "text": "กรอกสินค้าที่ขาย",
                        },
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "ดูยอดขายวันนี้",
                            "text": "รายงาน",
                        },
                    },
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "14px",
                "backgroundColor": "#FFF9EF",
                "contents": [
                    {
                        "type": "text",
                        "text": "FlowMate • ผู้ช่วยจัดการร้านค้า",
                        "align": "center",
                        "size": "xs",
                        "color": "#9A7B5B",
                    }
                ],
            },
        },
    )


def handle_menu_message(normalized_message):
    """
    จัดการคำทักทาย เมนู และข้อความช่วยเหลือ
    """

    if normalized_message in ["สวัสดี", "หวัดดี", "hello", "hi"]:
        return (
            "👋 สวัสดีค่ะ ยินดีต้อนรับสู่ FlowMate\n\n"
            "พิมพ์คำว่า “เมนู” เพื่อดูคำสั่งทั้งหมด"
        )

    if normalized_message == "ยอดขาย":
        return create_sales_flex_message()

    if normalized_message in [
        "กรอกยอดขายรวม",
        "บันทึกยอดขายรวม",
    ]:
        return (
            "💰 กรุณาพิมพ์ยอดขายรวมตามรูปแบบนี้\n\n"
            "ยอดขาย 2500\n\n"
            "ตัวอย่าง:\n"
            "ยอดขาย 850"
        )

    if normalized_message in [
        "กรอกสินค้าที่ขาย",
        "บันทึกสินค้าที่ขาย",
    ]:
        return (
            "🛍️ กรุณาพิมพ์สินค้าที่ขายตามรูปแบบนี้\n\n"
            "ขาย ชื่อสินค้า จำนวน ยอดขายรวม\n\n"
            "ตัวอย่าง:\n"
            "ขาย มัทฉะลาเต้ 2 110"
        )

    if normalized_message in ["เมนู", "menu"]:
        return create_main_menu_flex()

    if normalized_message == "ช่วยเหลือ":
        return (
            "🆘 วิธีใช้งาน FlowMate\n\n"
            "• เมนู\n"
            "• ยอดขาย 2500\n"
            "• ขาย มัทฉะลาเต้ 2 110\n"
            "• ค่าใช้จ่าย 350 ค่านม\n"
            "• ลูกค้า 5\n"
            "• รายงาน\n"
            "• รายงานสัปดาห์\n"
            "• รายงานเดือน\n"
            "• ช่วยเหลือ\n\n"
            "รูปแบบบันทึกสินค้า:\n"
            "ขาย ชื่อสินค้า จำนวน ยอดขายรวม"
        )

    return (
        "ขออภัยค่ะ FlowMate ยังไม่เข้าใจคำสั่งนี้\n\n"
        "พิมพ์คำว่า “เมนู” เพื่อดูคำสั่งที่ใช้ได้"
    )
