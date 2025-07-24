import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import pandas_ta as ta # Importamos a nova biblioteca

# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)

# --- FUNÇÃO DE ANÁLISE TÉCNICA ATUALIZADA COM RSI ---
def get_technical_signal(symbol):
    """
    Busca dados históricos, calcula médias móveis e RSI, 
    e gera um sinal de COMPRA ou VENDA com base em ambos os indicadores.
    """
    try:
        # 1. Buscar dados históricos (velas diárias), agora pegando 50 dias para dar mais dados ao RSI
        url = f'https://api.binance.us/api/v3/klines?symbol={symbol}&interval=1d&limit=50'
        response = requests.get(url )
        response.raise_for_status()
        data = response.json()

        # 2. Processar os dados com o Pandas
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])

        # 3. Calcular os Indicadores Técnicos
        # Adicionamos o cálculo do RSI (Índice de Força Relativa)
        df.ta.rsi(length=14, append=True) # Calcula o RSI de 14 dias e adiciona ao DataFrame
        df.ta.sma(length=10, append=True) # Média Móvel Curta (SMA_10)
        df.ta.sma(length=30, append=True) # Média Móvel Longa (SMA_30)

        # Remove linhas que não têm dados suficientes para os cálculos
        df.dropna(inplace=True)
        if df.empty:
            raise Exception("Não há dados suficientes para a análise após o cálculo dos indicadores.")

        # 4. Gerar o Sinal com a Lógica Combinada
        # Pegamos os valores mais recentes dos indicadores
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        signal_type = "NEUTRAL" # Sinal padrão

        # CONDIÇÃO DE COMPRA (MAIS RIGOROSA)
        # A média curta cruzou para CIMA da longa E o RSI está abaixo de 70 (não sobrecomprado)
        if last_row['SMA_10'] > last_row['SMA_30'] and prev_row['SMA_10'] <= prev_row['SMA_30']:
            if last_row['RSI_14'] < 70:
                signal_type = "BUY (Cruzamento Confirmado)"
            else:
                signal_type = "Cruzamento de Alta (Ignorado: RSI Sobrecomprado)"

        # CONDIÇÃO DE VENDA (MAIS RIGOROSA)
        # A média curta cruzou para BAIXO da longa E o RSI está acima de 30 (não sobrevendido)
        elif last_row['SMA_10'] < last_row['SMA_30'] and prev_row['SMA_10'] >= prev_row['SMA_30']:
            if last_row['RSI_14'] > 30:
                signal_type = "SELL (Cruzamento Confirmado)"
            else:
                signal_type = "Cruzamento de Baixa (Ignorado: RSI Sobrevendido)"
        
        # Se não houve cruzamento, definimos o estado de HOLD
        elif last_row['SMA_10'] > last_row['SMA_30']:
            signal_type = f"HOLD (Tendência de Alta, RSI: {last_row['RSI_14']:.2f})"
        else:
            signal_type = f"HOLD (Tendência de Baixa, RSI: {last_row['RSI_14']:.2f})"

        entry_price = last_row['close']
        
        return {
            "pair": symbol.replace("USDT", "/USDT"),
            "entry": round(entry_price, 4),
            "signal": signal_type,
            "stop": round(entry_price * 0.98, 4),
            "target": round(entry_price * 1.03, 4)
        }

    except Exception as e:
        print(f"Erro ao gerar sinal técnico para {symbol}: {e}")
        return {"pair": symbol.replace("USDT", "/USDT"), "signal": "ERROR", "entry": 0, "error_message": str(e)}

# Rota principal (sem alterações na estrutura)
@app.route("/signals")
def get_signals():
    try:
        symbols_to_process = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT"]
        signals = [get_technical_signal(symbol) for symbol in symbols_to_process]
        print("Sinais técnicos (com RSI) gerados com sucesso:")
        print(signals)
        return jsonify(signals)
    except Exception as e:
        print(f"Ocorreu um erro geral ao gerar os sinais: {e}")
        return jsonify({"error": f"Falha ao gerar sinais: {str(e)}"}), 500

# Bloco de execução principal (sem alterações)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
