from flask import Flask, jsonify
import random

app = Flask(__name__)

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
    app.run(debug=True)
