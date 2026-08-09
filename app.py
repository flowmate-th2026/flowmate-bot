import os

from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

from config import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET
from handlers import handle_text_message
from report_service import get_daily_sales_report
from services import (
    record_sale,
    record_expense,
    record_customer,
    record_product,
)

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


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

@app.route("/api/dashboard", methods=["GET"])
def dashboard_api():
    report = get_daily_sales_report()

    response = jsonify({
        "sales": report["total_sales"],
        "expense": report["total_expenses"],
        "profit": report["profit"],
        "customers": report["total_customers"],
        "top_products": report["top_products"],
        "latest_sales": report["latest_sales"],
        "latest_expenses": report["latest_expenses"],
        "latest_customers": report["latest_customers"],
    })

    response.headers["Access-Control-Allow-Origin"] = "*"

    return response

@app.route("/api/sales", methods=["POST"])
def create_sale_api():
    data = request.get_json(silent=True) or {}

    amount = data.get("amount")

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "จำนวนเงินไม่ถูกต้อง"
        }), 400

    if amount <= 0:
        return jsonify({
            "success": False,
            "message": "จำนวนเงินต้องมากกว่า 0"
        }), 400

    date_text, time_text = record_sale(amount)

    response = jsonify({
        "success": True,
        "message": "บันทึกยอดขายสำเร็จ",
        "amount": amount,
        "date": date_text,
        "time": time_text,
    })

    response.headers["Access-Control-Allow-Origin"] = "*"

    return response

@app.route("/api/expenses", methods=["POST", "OPTIONS"])
def create_expense_api():
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json(silent=True) or {}

    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        amount = 0

    description = str(data.get("description", "")).strip()

    if amount <= 0:
        return jsonify({
            "success": False,
            "message": "กรุณากรอกจำนวนเงินให้ถูกต้อง",
        }), 400

    if not description:
        return jsonify({
            "success": False,
            "message": "กรุณากรอกรายละเอียดค่าใช้จ่าย",
        }), 400

    date_text, time_text = record_expense(
        amount=amount,
        description=description,
    )

    response = jsonify({
        "success": True,
        "message": "บันทึกค่าใช้จ่ายสำเร็จ",
        "amount": amount,
        "description": description,
        "date": date_text,
        "time": time_text,
    })

    return response

@app.route("/api/customers", methods=["POST", "OPTIONS"])
def create_customer_api():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json(silent=True) or {}

    try:
        customer_count = int(data.get("customer_count", 0))
    except (TypeError, ValueError):
        customer_count = 0

    if customer_count <= 0:
        return jsonify({
            "success": False,
            "message": "กรุณากรอกจำนวนลูกค้าให้ถูกต้อง",
        }), 400

    date_text, time_text = record_customer(
        customer_count=customer_count,
    )

    response = jsonify({
        "success": True,
        "message": "บันทึกลูกค้าสำเร็จ",
        "customer_count": customer_count,
        "date": date_text,
        "time": time_text,
    })

    return response

@app.route("/api/products", methods=["POST", "OPTIONS"])
def create_product_api():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json(silent=True) or {}

    product_name = str(data.get("product_name", "")).strip()

    try:
        quantity = int(data.get("quantity", 0))
    except (TypeError, ValueError):
        quantity = 0

    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        amount = 0

    if not product_name:
        return jsonify({
            "success": False,
            "message": "กรุณากรอกชื่อสินค้า",
        }), 400

    if quantity <= 0:
        return jsonify({
            "success": False,
            "message": "กรุณากรอกจำนวนสินค้าให้ถูกต้อง",
        }), 400

    if amount <= 0:
        return jsonify({
            "success": False,
            "message": "กรุณากรอกยอดขายให้ถูกต้อง",
        }), 400

    date_text, time_text = record_product(
        product_name=product_name,
        quantity=quantity,
        amount=amount,
    )

    response = jsonify({
        "success": True,
        "message": "บันทึกการขายสินค้าสำเร็จ",
        "product_name": product_name,
        "quantity": quantity,
        "amount": amount,
        "date": date_text,
        "time": time_text,
    })

    return response

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    handle_text_message(event, line_bot_api)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
