from flask import Flask, request, jsonify
import hmac
import hashlib
import requests

app = Flask(__name__)

API_KEY = "DIN_API_NØKKEL"
API_SECRET = "DITT_API_SECRET"
API_URL = "https://api.crypto.com/v2/private/create-order"

def send_order(side, symbol, quantity):
    body = {
        "method": "private/create-order",
        "params": {
            "instrument_name": f"{symbol}_USDT",
            "side": side,
            "type": "MARKET",
            "quantity": quantity
        },
        "id": 11,
        "api_key": API_KEY,
        "nonce": str(int(time.time() * 1000))
    }

    # Signering
    sorted_params = "".join(f"{key}{value}" for key, value in sorted(body["params"].items()))
    to_sign = f"{body['id']}{API_KEY}{sorted_params}{body['nonce']}"
    signature = hmac.new(API_SECRET.encode(), to_sign.encode(), hashlib.sha256).hexdigest()
    body["sig"] = signature

    response = requests.post(API_URL, json=body)
    return response.json()
  }
  
  import time
  import base64

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
    import json
    body_json = json.dumps({
      "method": "private/create-order",
      "params": {
        "instrument_name": f"{symbol}_USDT",
        "side": side,
        "type": "market",
        "quantity": quantity
      },
      "id": 1
    })

    tstamp, sig = generate_signature(body_json, API_SECRET)
    headers = {
      "Content-Type": "application/json",
      "API-KEY": API_KEY,
      "API-TIMESTAMP": tstamp,
      "API-SIGNATURE": sig
    }

    response = requests.post(API_URL, data=body_json, headers=headers)
    print(response.status_code, response.text)
    return response.json()
  timestamp, signature = generate_signature(body_json, API_SECRET)

  headers = {
      "Content-Type": "application/json",
      "API-KEY": API_KEY,
      "API-TIMESTAMP": timestamp,
      "API-SIGN": signature
  }

  response = requests.post(API_URL, headers=headers, data=body_json)
  return response.json()


@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    signal = data.get("signal")
    symbol = data.get("symbol", "BTC")
    quantity = data.get("quantity", 0.001)

    if signal == "buy":
        return execute_order("buy", symbol, quantity)
    elif signal == "sell":
        return execute_order("sell", symbol, quantity)
    else:
        return {"error": "Ukjent signal"}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
