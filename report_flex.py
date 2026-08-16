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
        top_text = "ยังไม่มีข้อมูลการขายสินค้า"

    flex_contents = {
        "type": "bubble",
        "size": "kilo",

        "hero": {
            "type": "image",
            "url": "https://flowmate-bot.onrender.com/static/images/header-rooyod.jpg",
            "size": "full",
            "aspectRatio": "20:7",
            "aspectMode": "cover",
        },

        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF",
            "paddingAll": "14px",
            "spacing": "sm",
            "contents": [

                # REPORT TITLE
                {
                    "type": "text",
                    "text": "📊 สรุปยอดวันนี้",
                    "weight": "bold",
                    "size": "md",
                    "color": "#0F2B5B",
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
                            "cornerRadius": "12px",
                            "paddingAll": "10px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "ยอดขาย",
                                    "size": "xs",
                                    "color": "#64748B",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(sales)}",
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": "#2563EB",
                                    "margin": "xs",
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
                            "cornerRadius": "12px",
                            "paddingAll": "10px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "ค่าใช้จ่าย",
                                    "size": "xs",
                                    "color": "#64748B",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(expense)}",
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": "#DB2777",
                                    "margin": "xs",
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
                            "cornerRadius": "12px",
                            "paddingAll": "10px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "ลูกค้า",
                                    "size": "xs",
                                    "color": "#64748B",
                                },
                                {
                                    "type": "text",
                                    "text": str(customer),
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": "#2563EB",
                                    "margin": "xs",
                                },
                            ],
                        },
                                                # PROFIT
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "backgroundColor": "#F0FDF4",
                            "cornerRadius": "12px",
                            "paddingAll": "10px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "กำไร",
                                    "size": "xs",
                                    "color": "#64748B",
                                },
                                {
                                    "type": "text",
                                    "text": f"฿{money(profit)}",
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": "#16A34A",
                                    "margin": "xs",
                                    "wrap": True,
                                },
                            ],
                        },
                    ],
                },

                # TOP PRODUCT
                {
                    "type": "box",
                    "layout": "horizontal",
                    "backgroundColor": "#F8FAFC",
                    "cornerRadius": "12px",
                    "paddingAll": "10px",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🏆",
                            "size": "sm",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": top_text,
                            "size": "xs",
                            "color": "#475569",
                            "wrap": True,
                            "margin": "sm",
                            "flex": 1,
                        },
                    ],
                },

                # BUTTONS
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "margin": "sm",
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

                        {
                            "type": "button",
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "เมนู",
                                "text": "เมนู",
                            },
                        },
                    ],
                },
            ],
        },
    }

    return FlexSendMessage(
        alt_text="สรุปยอดวันนี้",
        contents=flex_contents,
    )