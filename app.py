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
    melding = data.get('message', '').lower()

    logg = ""

    if "kjøpssignal" in melding:
        if simulert_konto["USDC"] >= 100:
            simulert_konto["BTC"] += 0.001
            simulert_konto["USDC"] -= 100
            logg = "SIMULERT KJØP: 0.001 BTC for 100 USDC"
        else:
            logg = "Ikke nok USDC til kjøp"

    elif "salg" in melding:
        if simulert_konto["BTC"] >= 0.001:
            simulert_konto["BTC"] -= 0.001
            simulert_konto["USDC"] += 100
            logg = "SIMULERT SALG: 0.001 BTC solgt for 100 USDC"
        else:
            logg = "Ikke nok BTC til salg"
    else:
        logg = "Ukjent melding mottatt: " + melding

    print(logg)
    print("Ny saldo:", simulert_konto)

    return jsonify({
        "status": "OK",
        "melding": melding,
        "handling": logg,
        "saldo": simulert_konto
    })

if __name__ == '__main__':
    app.run()
