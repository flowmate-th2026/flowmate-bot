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
    user_message = event.message.text

    if user_message == "สวัสดี":
        reply = "👋 สวัสดีค่ะ ยินดีต้อนรับสู่ FlowMate"
    else:
        reply = f"คุณพิมพ์ว่า: {user_message}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )
if __name__== "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000))
    )
