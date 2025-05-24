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
