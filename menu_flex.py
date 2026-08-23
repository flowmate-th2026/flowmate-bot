from linebot.models import FlexSendMessage

def create_main_menu_flex():
    return FlexSendMessage(
        alt_text="เมนูหลัก RooYod",
        contents={
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#FFFFFF",
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "text",
                        "text": "RooYod by FlowMate",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1E3A8A"
                    },
                    {
                        "type": "text",
                        "text": "ผู้ช่วยดูยอดร้าน เข้าใจง่ายใน LINE",
                        "size": "sm",
                        "color": "#6B7280",
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },

                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "lg",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "color": "#2563EB",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "💰 ยอดขาย",
                                    "text": "บันทึกยอดขาย"
                                }
                            },
                            {
                                "type": "button",
                                "style": "primary",
                                "color": "#2563EB",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "🛒 ขายสินค้า",
                                    "text": "บันทึกสินค้าที่ขาย"
                                }
                            }
                        ]
                    },

                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "💸 ค่าใช้จ่าย",
                                    "text": "ค่าใช้จ่าย"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "👥 ลูกค้า",
                                    "text": "ลูกค้า"
                                }
                            }
                        ]
                    },

                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "color": "#16A34A",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "📊 รายงาน",
                                    "text": "รายงาน"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "🏪 ร้านของฉัน",
                                    "text": "โปรไฟล์ร้าน"
                                }
                            }
                        ]
                    },

                    {
                        "type": "separator",
                        "margin": "lg"
                    },

                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "link",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "❓ วิธีใช้",
                                    "text": "ช่วยเหลือ"
                                }
                            },
                            {
                                "type": "button",
                                "style": "link",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "✨ ทดลองใช้",
                                    "text": "สถานะทดลองใช้"
                                }
                            }
                        ]
                    }
                ]
            }
        }
    )