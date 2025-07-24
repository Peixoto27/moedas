# (Cole aqui o código completo do main.py que eu forneci na mensagem anterior)
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)
CORS(app)

def get_technical_signal(symbol, timeframe='1d'):
    timeframe_limits = {'1h': 100, '4h': 100, '1d': 50, '1w': 50}
    limit = timeframe_limits.get(timeframe, 50)
    try:
        url = f'https://api.binance.us/api/v3/klines?symbol={symbol}&interval={timeframe}&limit={limit}'
        response = requests.get(url )
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        df.ta.rsi(length=14, append=True)
        df.ta.sma(length=10, append=True)
        df.ta.sma(length=30, append=True)
        df.dropna(inplace=True)
        if df.empty: raise Exception("Não há dados suficientes para a análise.")
        last_row, prev_row = df.iloc[-1], df.iloc[-2]
        signal_type = "NEUTRAL"
        if last_row['SMA_10'] > last_row['SMA_30'] and prev_row['SMA_10'] <= prev_row['SMA_30']:
            signal_type = "BUY (Cruzamento Confirmado)" if last_row['RSI_14'] < 70 else "Cruzamento de Alta (Ignorado: RSI Sobrecomprado)"
        elif last_row['SMA_10'] < last_row['SMA_30'] and prev_row['SMA_10'] >= prev_row['SMA_30']:
            signal_type = "SELL (Cruzamento Confirmado)" if last_row['RSI_14'] > 30 else "Cruzamento de Baixa (Ignorado: RSI Sobrevendido)"
        elif last_row['SMA_10'] > last_row['SMA_30']:
            signal_type = f"HOLD (Tendência de Alta, RSI: {last_row['RSI_14']:.2f})"
        else:
            signal_type = f"HOLD (Tendência de Baixa, RSI: {last_row['RSI_14']:.2f})"
        entry_price = last_row['close']
        return {"pair": symbol.replace("USDT", "/USDT"), "entry": round(entry_price, 4), "signal": signal_type, "stop": round(entry_price * 0.98, 4), "target": round(entry_price * 1.03, 4)}
    except Exception as e:
        print(f"Erro ao gerar sinal para {symbol} com timeframe {timeframe}: {e}")
        return {"pair": symbol.replace("USDT", "/USDT"), "signal": "ERROR", "entry": 0, "error_message": str(e)}

@app.route("/signals")
def get_stable_signals():
    try:
        symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT"]
        signals = [get_technical_signal(s, '1d') for s in symbols]
        return jsonify(signals)
    except Exception as e:
        return jsonify({"error": f"Falha ao gerar sinais estáveis: {str(e)}"}), 500

@app.route("/signals_v2")
def get_dynamic_signals():
    timeframe = request.args.get('timeframe', '1d')
    if timeframe not in ['1h', '4h', '1d', '1w']:
        return jsonify({"error": "Timeframe inválido."}), 400
    try:
        symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT"]
        signals = [get_technical_signal(s, timeframe) for s in symbols]
        return jsonify(signals)
    except Exception as e:
        return jsonify({"error": f"Falha ao gerar sinais dinâmicos: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
