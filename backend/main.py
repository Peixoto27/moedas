import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import numpy as np

# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)

# --- FUNÇÃO DE ANÁLISE TÉCNICA ---
def get_technical_signal(symbol):
    """
    Busca dados históricos, calcula médias móveis e gera um sinal de COMPRA ou VENDA.
    """
    try:
        # 1. Buscar dados históricos (velas diárias)
        # klines (velas) com intervalo de 1 dia ('1d'), pegando os últimos 30 dias.
        url = f'https://api.binance.us/api/v3/klines?symbol={symbol}&interval=1d&limit=30'
        response = requests.get(url )
        response.raise_for_status()
        data = response.json()

        # 2. Processar os dados com o Pandas
        # Criamos um DataFrame do Pandas para facilitar os cálculos.
        # A coluna 'Close' (preço de fechamento) é a que nos interessa.
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])

        # 3. Calcular as Médias Móveis
        # Média Curta de 10 dias e Média Longa de 30 dias.
        short_window = 10
        long_window = 30
        df['short_mavg'] = df['close'].rolling(window=short_window, min_periods=1).mean()
        df['long_mavg'] = df['close'].rolling(window=long_window, min_periods=1).mean()

        # 4. Gerar o Sinal com base no cruzamento
        # Pegamos os valores das médias do último dia e do penúltimo dia.
        last_short_mavg = df['short_mavg'].iloc[-1]
        last_long_mavg = df['long_mavg'].iloc[-1]
        prev_short_mavg = df['short_mavg'].iloc[-2]
        prev_long_mavg = df['long_mavg'].iloc[-2]

        signal_type = "NEUTRAL" # Sinal padrão
        # Cruzamento para CIMA (Sinal de Compra)
        if last_short_mavg > last_long_mavg and prev_short_mavg <= prev_long_mavg:
            signal_type = "BUY"
        # Cruzamento para BAIXO (Sinal de Venda)
        elif last_short_mavg < last_long_mavg and prev_short_mavg >= prev_long_mavg:
            signal_type = "SELL"
        # Se não houve cruzamento, mantemos a tendência atual
        elif last_short_mavg > last_long_mavg:
            signal_type = "HOLD (Tendência de Alta)"
        else:
            signal_type = "HOLD (Tendência de Baixa)"

        # O preço de entrada será o preço de fechamento mais recente
        entry_price = df['close'].iloc[-1]
        
        return {
            "pair": symbol.replace("USDT", "/USDT"),
            "entry": round(entry_price, 4), # Aumentar precisão para moedas mais baratas
            "signal": signal_type,
            "stop": round(entry_price * 0.98, 4),
            "target": round(entry_price * 1.03, 4)
        }

    except Exception as e:
        print(f"Erro ao gerar sinal técnico para {symbol}: {e}")
        # Se a análise falhar, retorna um sinal de erro para essa moeda
        return {
            "pair": symbol.replace("USDT", "/USDT"),
            "signal": "ERROR",
            "entry": 0,
            "error_message": str(e)
        }

# Rota principal que agora usa a nova função de análise
@app.route("/signals")
def get_signals():
    """Endpoint que retorna uma lista de sinais baseados em análise técnica."""
    try:
        symbols_to_process = [
            "BTCUSDT", 
            "ETHUSDT", 
            "XRPUSDT",
            "SOLUSDT",
            "ADAUSDT"
        ]
        
        # Usamos a nova função get_technical_signal
        signals = [get_technical_signal(symbol) for symbol in symbols_to_process]
        
        print("Sinais técnicos gerados com sucesso:")
        print(signals)
        return jsonify(signals)
    except Exception as e:
        print(f"Ocorreu um erro geral ao gerar os sinais: {e}")
        return jsonify({"error": f"Falha ao gerar sinais: {str(e)}"}), 500

# Bloco de execução principal
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

