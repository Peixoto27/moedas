from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def get_crypto_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def generate_signal(symbol):
    price = get_crypto_price(symbol)
    
    # Exemplo simples de lógica
    signal_type = "BUY" if symbol == "BTCUSDT" else "SELL"
    stop = round(price * 0.98, 2)
    target = round(price * 1.03, 2)

    return {
        "pair": symbol.replace("USDT", "/USDT"),
        "entry": round(price, 2),
        "signal": signal_type,
        "stop": stop,
        "target": target
    }

@app.route("/signals")
def get_signals():
    try:
        signals = [
            generate_signal("BTCUSDT"),
            generate_signal("ETHUSDT"),
            generate_signal("XRPUSDT")
        ]
        return jsonify(signals)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
