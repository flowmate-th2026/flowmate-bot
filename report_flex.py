from linebot.models import FlexSendMessage


def create_report_flex(
    sales,
    expense,
    customer,
    profit,
    top_products,
):

    def money(value):
        return f"{float(value):,.2f}"

    flex_contents = {
        "type": "bubble",
        "size": "mega",

        "styles": {
            "header": {
                "backgroundColor": "#EAF4FF"
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
                    "text": "📊 รายงานวันนี้",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1E3A8A"
                },
                {
                    "type": "text",
                    "text": "สรุปยอดขายและกำไรของร้าน",
                    "size": "sm",
                    "color": "#666666",
                    "margin": "md"
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
                            "text": "💰 ยอดขาย",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"฿{money(sales)}",
                            "align": "end",
                            "weight": "bold",
                            "color": "#1677FF"
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
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": "💸 ค่าใช้จ่าย"
                        },
                        {
                            "type": "text",
                            "text": f"฿{money(expense)}",
                            "align": "end",
                            "color": "#D9368B"
                        }
                    ]
                },

                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "👥 ลูกค้า"
                        },
                        {
                            "type": "text",
                            "text": str(customer),
                            "align": "end"
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
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📈 กำไร",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"฿{money(profit)}",
                            "align": "end",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#00AA55"
                        }
                    ]
                },

{
    "type": "separator",
    "margin": "xl",
},
{
    "type": "text",
    "text": "🏆 สินค้าขายดีวันนี้",
    "weight": "bold",
    "size": "md",
    "color": "#1E3A8A",
    "margin": "xl",
},
{
    "type": "box",
    "layout": "vertical",
    "margin": "md",
    "spacing": "sm",
    "contents": (
        [
            {
                "type": "text",
                "text": (
                    f"{medal} {product['name']} "
                    f"— {product['quantity']} ชิ้น"
                ),
                "size": "sm",
                "color": "#374151",
                "wrap": True,
            }
            for medal, product in zip(
                ["🥇", "🥈", "🥉"],
                top_products,
            )
        ]
        if top_products
        else [
            {
                "type": "text",
                "text": "ยังไม่มีข้อมูลการขายสินค้าในวันนี้",
                "size": "sm",
                "color": "#6B7280",
                "wrap": True,
            }
        ]
    ),
},       
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
                    "color": "#1677FF",
                    "action": {
                        "type": "message",
                        "label": "📅 รายงานสัปดาห์",
                        "text": "รายงานสัปดาห์"
                    }
                },

                {
                    "type": "button",
                    "style": "primary",
                    "margin": "sm",
                    "color": "#00AA55",
                    "action": {
                        "type": "message",
                        "label": "📆 รายงานเดือน",
                        "text": "รายงานเดือน"
                    }
                },

                {
                    "type": "button",
                    "style": "secondary",
                    "margin": "sm",
                    "action": {
                        "type": "message",
                        "label": "🏠 กลับเมนู",
                        "text": "เมนู"
                    }
                },

                {
                    "type": "text",
                    "text": "FlowMate • Smart Business Assistant",
                    "size": "xs",
                    "color": "#999999",
                    "align": "center",
                    "margin": "lg"
                }

            ]
        }

    }

    return FlexSendMessage(
        alt_text="รายงานประจำวัน",
        contents=flex_contents
    )
