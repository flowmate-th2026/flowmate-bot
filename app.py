import os
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
app = Flask(__name__)
@app.route("/")
def home():
    return "Flowmate Bot is running!"
@app.route("/callback", methods=["POST"])
def callback():
    return "OK"
if __name__== "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000))
    )
