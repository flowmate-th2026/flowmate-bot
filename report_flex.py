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

    if top_products:
        top_text = (
            f"🥇 {top_products[0]['name']} "
            f"— {top_products[0]['quantity']} ชิ้น"
        )
    else:
        top_text = "ยังไม่มีข้อมูลการขายสินค้าในวันนี้"

    flex_contents = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF",
            "paddingAll": "16px",
            "spacing": "md",
            "contents": [

                # HEADER
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
                                    "text": "RooYod by FlowMate",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#2563EB",
                                },
                                {
                                    "type": "text",
                                    "text": "ผู้ช่วยจัดการร้านค้า",
                                    "size": "xs",
                                    "color": "#94A3B8",
                                    "margin": "xs",
                                },
                            ],
                        },
                        {
                            "type": "text",
                            "text": "🤖",
                            "size": "lg",
                        },
                    ],
                },

                # TITLE
                {
                    "type": "box",
                    "layout": "horizontal",
                    "alignItems": "center",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📊 สรุปยอดวันนี้",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#0F2B5B",
                            "flex": 1,
                            "wrap": True,
                        },
                        {
                            "type": "text",
                            "text": "วันนี้",
                            "size": "xs",
                            "color": "#64748B",
                            "align": "end",
                            "margin": "md",
                        },
                    ],
                },
                {
                    "type": "text",
                    "text": "สรุปยอดขายและกำไรของร้าน",
                    "size": "xs",
                    "color": "#64748B",
                    "margin": "xs",
                },

                # ROW 1
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#EFF6FF",
                            "cornerRadius": "14px",
                            "paddingAll": "12px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🛍️ ยอดขาย",
                                    "size": "xs",
                                    "color": "#475569",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(sales)}",
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": "#2563EB",
                                    "margin": "sm",
                                    "wrap": True,
                                },
                            ],
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#FDF2F8",
                            "cornerRadius": "14px",
                            "paddingAll": "12px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🧾 ค่าใช้จ่าย",
                                    "size": "xs",
                                    "color": "#475569",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(expense)}",
                                    "size": "lg",
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
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#EFF6FF",
                            "cornerRadius": "14px",
                            "paddingAll": "12px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "👥 ลูกค้า",
                                    "size": "xs",
                                    "color": "#475569",
                                },
                                {
                                    "type": "text",
                                    "text": str(customer),
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": "#2563EB",
                                    "margin": "sm",
                                },
                            ],
                        },
                                                {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#F0FDF4",
                            "cornerRadius": "14px",
                            "paddingAll": "12px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "📈 กำไร",
                                    "size": "xs",
                                    "color": "#475569",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(profit)}",
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": "#16A34A",
                                    "margin": "sm",
                                    "wrap": True,
                                },
                            ],
                        },
                    ],
                },

                # TOP PRODUCT
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#F8FAFC",
                    "cornerRadius": "14px",
                    "paddingAll": "12px",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🏆 สินค้าขายดีวันนี้",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#1E40AF",
                        },
                        {
                            "type": "text",
                            "text": top_text,
                            "size": "xs",
                            "color": "#475569",
                            "wrap": True,
                            "margin": "sm",
                        },
                    ],
                },

                # BUTTONS ROW
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "color": "#2563EB",
                            "action": {
                                "type": "message",
                                "label": "สัปดาห์",
                                "text": "รายงานสัปดาห์",
                            },
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "color": "#16A34A",
                            "action": {
                                "type": "message",
                                "label": "เดือน",
                                "text": "รายงานเดือน",
                            },
                        },
                    ],
                },

                # MENU BUTTON
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "🏠 กลับเมนู",
                        "text": "เมนู",
                    },
                },
            ],
        },
    }

    return FlexSendMessage(
        alt_text="สรุปยอดวันนี้",
        contents=flex_contents,
    )