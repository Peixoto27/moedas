from flask import Flask, jsonify
from flask_cors import CORS  # ← Linha 2
import random
import os

app = Flask(__name__)
CORS(app)  # ← Logo depois de criar o app

@app.route("/signals")
def get_signals():
    sample = {
        "pair": "BTC/USDT",
        "signal": "BUY",
        "entry": round(random.uniform(57000, 59000), 2),
        "target": round(random.uniform(59000, 61000), 2),
        "stop": round(random.uniform(56000, 57000), 2)
    }
    return jsonify(sample)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
