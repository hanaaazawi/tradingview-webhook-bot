from flask import Flask, request, jsonify
import hmac
import hashlib
import requests
import time
import base64
import json

app = Flask(__name__)

API_KEY = "DIN_API_NØKKEL"
API_SECRET = "DITT_API_SECRET"
API_URL = "https://api.crypto.com/v2/private/create-order"

def generate_signature(body, api_secret):
    tstamp = str(int(time.time() * 1000))
    payload = tstamp + "\n" + body
    signature = hmac.new(
        bytes(api_secret, encoding='utf-8'),
        msg=bytes(payload, encoding='utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return tstamp, signature

def execute_order(side, symbol, quantity):
    body_json = json.dumps({
        "method": "private/create-order",
        "params": {
            "instrument_name": f"{symbol}_USDT",
            "side": side,
            "type": "MARKET",
            "quantity": quantity
        }
    })

    timestamp, signature = generate_signature(body_json, API_SECRET)
    headers = {
        "Content-Type": "application/json",
        "API-KEY": API_KEY,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": signature
    }

    response = requests.post(API_URL, headers=headers, data=body_json)
    print(response.status_code, response.text)
    return response.json()

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    signal = data.get("signal")
    symbol = data.get("symbol", "BTC")
    quantity = data.get("quantity", 0.001)

    if signal == "buy":
        return jsonify(execute_order("BUY", symbol, quantity))
    elif signal == "sell":
        return jsonify(execute_order("SELL", symbol, quantity))
    else:
        return jsonify({"error": "Invalid signal"}), 400
