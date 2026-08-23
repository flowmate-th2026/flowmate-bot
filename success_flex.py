from linebot.models import FlexSendMessage


def create_success_flex(
    record_type,
    amount,
    description,
    date_text,
    time_text,
    category="อื่นๆ",
):
    """
    สร้าง Flex Message ยืนยันการบันทึกรายการสำเร็จ

    record_type: "ยอดขาย" หรือ "ค่าใช้จ่าย"
    amount: จำนวนเงิน
    description: รายละเอียดรายการ
    date_text: วันที่
    time_text: เวลา
    category: หมวดหมู่
    """

    try:
        amount_number = float(amount)
        formatted_amount = f"{amount_number:,.2f}"
    except (TypeError, ValueError):
        formatted_amount = str(amount)

    if record_type == "ยอดขาย":
        accent_color = "#1677FF"
        light_color = "#EAF3FF"
        title_text = "บันทึกยอดขายสำเร็จ"
        icon_text = "💰"
    else:
        accent_color = "#D9368B"
        light_color = "#FFF0F6"
        title_text = "บันทึกค่าใช้จ่ายสำเร็จ"
        icon_text = "🧾"

    flex_contents = {
        "type": "bubble",
        "size": "mega",
        "styles": {
            "header": {
                "backgroundColor": light_color
            },
            "body": {
                "backgroundColor": "#FFFFFF"
            },
            "footer": {
                "backgroundColor": "#FFFFFF"
            }
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": f"{icon_text} จดสำเร็จ ✅",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#222222"
                },
                {
                    "type": "text",
                    "text": "อย่าลืมตรวจสอบรายละเอียดอีกครั้งนะคะ",
                    "size": "sm",
                    "color": "#666666",
                    "margin": "md",
                    "wrap": True
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": record_type,
                            "size": "sm",
                            "weight": "bold",
                            "color": "#FFFFFF",
                            "align": "center",
                            "gravity": "center"
                        }
                    ],
                    "backgroundColor": accent_color,
                    "cornerRadius": "20px",
                    "paddingStart": "14px",
                    "paddingEnd": "14px",
                    "paddingTop": "5px",
                    "paddingBottom": "5px",
                    "width": "100px"
                },
                {
                    "type": "text",
                    "text": title_text,
                    "weight": "bold",
                    "size": "lg",
                    "color": "#333333",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"{date_text} เวลา {time_text}",
                    "size": "sm",
                    "color": "#777777",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#DDDDDD"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xl",
                    "contents": [
                        {
                            "type": "text",
                            "text": "รายการ",
                            "size": "sm",
                            "color": "#777777",
                            "flex": 2
                        },
                        {
                            "type": "text",
                            "text": str(description),
                            "size": "md",
                            "weight": "bold",
                            "color": "#333333",
                            "align": "end",
                            "wrap": True,
                            "flex": 4
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมวดหมู่",
                            "size": "sm",
                            "color": "#777777",
                            "flex": 2
                        },
                        {
                            "type": "text",
                            "text": str(category),
                            "size": "md",
                            "color": "#333333",
                            "align": "end",
                            "wrap": True,
                            "flex": 4
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#DDDDDD"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xl",
                    "contents": [
                        {
                            "type": "text",
                            "text": "จำนวนเงิน",
                            "size": "md",
                            "weight": "bold",
                            "color": "#333333",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": f"฿{formatted_amount}",
                            "size": "xxl",
                            "weight": "bold",
                            "color": accent_color,
                            "align": "end"
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": accent_color,
                    "action": {
                        "type": "message",
                        "label": "ดูรายงานวันนี้",
                        "text": "รายงานวันนี้"
                    }
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "margin": "sm",
                    "action": {
                        "type": "message",
                        "label": "กลับไปที่เมนู",
                        "text": "เมนู"
                    }
                },
                {
                    "type": "text",
                    "text": "RooYod by FlowMate • ผู้ช่วยดูยอดร้าน",
                    "size": "xs",
                    "color": "#999999",
                    "align": "center",
                    "margin": "lg"
                }
            ]
        }
    }

    return FlexSendMessage(
        alt_text=f"{title_text} ฿{formatted_amount}",
        contents=flex_contents,
    )
