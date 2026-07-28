import os

from flask import Flask, request
from dotenv import load_dotenv

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
app = Flask(__name__)
load_dotenv()

line_bot_api = LineBotApi(
    os.getenv("CHANNEL_ACCESS_TOKEN")
)
handler = WebhookHandler(
    os.getenv("CHANNEL_SECRET")
)
@app.route("/")
def home():
    return "Flowmate Bot is running!"
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400
    return "OK"
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message in ["สวัสดี", "หวัดดี", "hello", "hi"]:
        reply = (
            "👋 สวัสดีค่ะ ยินดีต้อนรับสู่ FlowMate\n\n"
            "พิมพ์คำว่า “เมนู” เพื่อดูคำสั่งทั้งหมด"
        )

    elif user_message in ["เมนู", "menu"]:
        reply = (
            "🤖 เมนู FlowMate\n\n"
            "1️⃣ พิมพ์ “ยอดขาย” เพื่อบันทึกยอดขาย\n"
            "2️⃣ พิมพ์ “รายงาน” เพื่อดูรายงานร้านค้า\n"
            "3️⃣ พิมพ์ “ช่วยเหลือ” เพื่อดูวิธีใช้งาน\n\n"
            "ตอนนี้ระบบกำลังอยู่ในช่วงพัฒนา 💚"
        )

    elif user_message == "ยอดขาย":
        reply = (
            "💰 ระบบบันทึกยอดขาย\n\n"
            "ตัวอย่างการใช้งาน:\n"
            "ยอดขาย 1200\n\n"
            "วันนี้เราจะเริ่มสร้างระบบนี้กันค่ะ"
        )

    elif user_message == "รายงาน":
        reply = (
            "📊 ระบบรายงานร้านค้า\n\n"
            "ในอนาคต FlowMate จะสรุป:\n"
            "• ยอดขายประจำวัน\n"
            "• จำนวนลูกค้า\n"
            "• สินค้าขายดี\n"
            "• กำไรและค่าใช้จ่าย"
        )

    elif user_message == "ช่วยเหลือ":
        reply = (
            "🆘 วิธีใช้งาน FlowMate\n\n"
            "พิมพ์คำสั่งต่อไปนี้ได้เลย:\n"
            "• เมนู\n"
            "• ยอดขาย\n"
            "• รายงาน\n"
            "• ช่วยเหลือ"
        )

    else:
        reply = (
            "ขออภัยค่ะ FlowMate ยังไม่เข้าใจข้อความนี้\n\n"
            "พิมพ์คำว่า “เมนู” เพื่อดูคำสั่งที่ใช้ได้"
        )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )
if __name__== "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000))
    )
