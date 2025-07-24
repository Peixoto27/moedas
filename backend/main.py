from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def get_crypto_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    response.raise_for_status()  # Lança erro se a resposta for inválida
    data = response.json()
    return float(data['price'])

def generate_signal(symbol):
    price = get_crypto_price(symbol)
    signal_type = "BUY" if symbol in ["BTCUSDT", "ETHUSDT", "XRPUSDT"] else "SELL"
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
        print("Gerando sinais...")
        print(signals)
        return jsonify(signals)
    except Exception as e:
        print("Erro ao gerar sinais:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
