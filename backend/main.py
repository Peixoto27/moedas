from flask import Flask, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

@app.route("/signals", methods=["GET"])
def get_signals():
    signal = {
        "pair": "BTC/USDT",
        "signal": "BUY",
        "entry": round(random.uniform(57000, 59000), 2),
        "target": round(random.uniform(59000, 61000), 2),
        "stop": round(random.uniform(56000, 57000), 2)
    }
    return jsonify(signal)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
