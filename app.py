from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulert balanse
simulert_konto = {
    "BTC": 0.0,
    "USDC": 1000.0  # Startbalanse
}

@app.route('/', methods=['GET'])
def home():
    return "Bot kjører OK 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    action = data.get("action", "").lower()
    symbol = data.get("symbol", "BTCUSD").upper()

    if action == "buy":
        pris = 50000  # Simulert pris
        antall = simulert_konto["USDC"] / pris
        simulert_konto["BTC"] += antall
        simulert_konto["USDC"] = 0
        return jsonify({"message": f"Kjøpte {antall:.6f} BTC", "balanse": simulert_konto})

    elif action == "sell":
        pris = 50000  # Simulert pris
        usdc = simulert_konto["BTC"] * pris
        simulert_konto["USDC"] += usdc
        simulert_konto["BTC"] = 0
        return jsonify({"message": f"Solgte for {usdc:.2f} USDC", "balanse": simulert_konto})

    else:
        return jsonify({"message": "Ukjent handling"}), 400
