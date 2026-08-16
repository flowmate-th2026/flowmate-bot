from linebot.models import FlexSendMessage


def create_report_flex(
    sales,
    expense,
    customer,
    profit,
    top_products,
):
    """
    RooYod Daily Report Flex Message
    Day 36 - New Design
    """

    def money(value):
        return f"{float(value):,.2f}"

    if top_products:
        product_contents = [
            {
                "type": "text",
                "text": (
                    f"{medal} {product['name']} "
                    f"— {product['quantity']} ชิ้น"
                ),
                "size": "sm",
                "color": "#374151",
                "wrap": True,
                "margin": "sm",
            }
            for medal, product in zip(
                ["🥇", "🥈", "🥉"],
                top_products,
            )
        ]
    else:
        product_contents = [
            {
                "type": "text",
                "text": "ยังไม่มีข้อมูลการขายสินค้าในวันนี้",
                "size": "sm",
                "color": "#6B7280",
                "wrap": True,
                "margin": "sm",
            }
        ]

    flex_contents = {
        "type": "bubble",
        "size": "mega",

        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF",
            "paddingAll": "18px",
            "spacing": "md",
            "contents": [

                # BRAND
                {
                    "type": "box",
                    "layout": "horizontal",
                    "alignItems": "center",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "RooYod",
                                    "weight": "bold",
                                    "size": "xl",
                                    "color": "#2563EB",
                                },
                                {
                                    "type": "text",
                                    "text": "by FlowMate",
                                    "size": "xs",
                                    "color": "#64748B",
                                    "margin": "xs",
                                },
                            ],
                        },
                        {
                            "type": "text",
                            "text": "🤖",
                            "size": "xl",
                            "align": "end",
                        },
                    ],
                },

                # TITLE
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📊 สรุปยอดวันนี้",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#0F2B5B",
                        },
                        {
                            "type": "text",
                            "text": "สรุปยอดขายและกำไรของร้าน",
                            "size": "sm",
                            "color": "#64748B",
                            "margin": "sm",
                        },
                    ],
                },

                # ROW 1
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [

                        # SALES
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#EFF6FF",
                            "cornerRadius": "16px",
                            "paddingAll": "14px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🛍️",
                                    "size": "lg",
                                },
                                {
                                    "type": "text",
                                    "text": "ยอดขาย",
                                    "size": "sm",
                                    "color": "#475569",
                                    "margin": "sm",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(sales)}",
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": "#2563EB",
                                    "margin": "sm",
                                    "wrap": True,
                                },
                            ],
                        },

                        # EXPENSE
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#FDF2F8",
                            "cornerRadius": "16px",
                            "paddingAll": "14px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🧾",
                                    "size": "lg",
                                },
                                {
                                    "type": "text",
                                    "text": "ค่าใช้จ่าย",
                                    "size": "sm",
                                    "color": "#475569",
                                    "margin": "sm",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(expense)}",
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": "#DB2777",
                                    "margin": "sm",
                                    "wrap": True,
                                },
                            ],
                        },
                    ],
                },

                # ROW 2
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [

                        # CUSTOMER
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#EFF6FF",
                            "cornerRadius": "16px",
                            "paddingAll": "14px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "👥",
                                    "size": "lg",
                                },
                                {
                                    "type": "text",
                                    "text": "ลูกค้า",
                                    "size": "sm",
                                    "color": "#475569",
                                    "margin": "sm",
                                },
                                {
                                    "type": "text",
                                    "text": str(customer),
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": "#2563EB",
                                    "margin": "sm",
                                },
                            ],
                        },

                                                # PROFIT
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#F0FDF4",
                            "cornerRadius": "16px",
                            "paddingAll": "14px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "📈",
                                    "size": "lg",
                                },
                                {
                                    "type": "text",
                                    "text": "กำไร",
                                    "size": "sm",
                                    "color": "#475569",
                                    "margin": "sm",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(profit)}",
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": "#16A34A",
                                    "margin": "sm",
                                    "wrap": True,
                                },
                            ],
                        },
                    ],
                },

                # TOP PRODUCTS
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#F8FAFC",
                    "cornerRadius": "16px",
                    "paddingAll": "16px",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🏆 สินค้าขายดีวันนี้",
                            "weight": "bold",
                            "size": "md",
                            "color": "#1E40AF",
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "sm",
                            "contents": product_contents,
                        },
                    ],
                },

                # WEEKLY REPORT
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": "#2563EB",
                    "margin": "md",
                    "action": {
                        "type": "message",
                        "label": "📅 รายงานสัปดาห์",
                        "text": "รายงานสัปดาห์",
                    },
                },

                # MONTHLY REPORT
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": "#16A34A",
                    "margin": "sm",
                    "action": {
                        "type": "message",
                        "label": "📆 รายงานเดือน",
                        "text": "รายงานเดือน",
                    },
                },

                # BACK TO MENU
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "margin": "sm",
                    "action": {
                        "type": "message",
                        "label": "🏠 กลับเมนู",
                        "text": "เมนู",
                    },
                },

                # FOOTER
                {
                    "type": "text",
                    "text": "RooYod by FlowMate • ผู้ช่วยจัดการร้านค้า",
                    "size": "xxs",
                    "color": "#94A3B8",
                    "align": "center",
                    "margin": "lg",
                },
            ],
        },
    }

    return FlexSendMessage(
        alt_text="สรุปยอดวันนี้",
        contents=flex_contents,
    )