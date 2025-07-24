import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests

# Inicializa a aplicação Flask
app = Flask(__name__)

# Habilita o CORS
CORS(app)

# --- FUNÇÃO ALTERADA PARA USAR A API DA BINANCE.US ---
def get_crypto_price(symbol):
    """Busca o preço atual de um par de moedas na API da Binance.US."""
    
    # ALTERAÇÃO CRUCIAL: Apontando para a API da Binance para os EUA (binance.us)
    # Esta é a API correta para usar a partir de servidores localizados nos EUA.
    url = f'https://api.binance.us/api/v3/ticker/price?symbol={symbol}'
    
    try:
        response = requests.get(url )
        # Lança um erro se a resposta da API for inválida (ex: 404, 500)
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
        
    except requests.exceptions.RequestException as e:
        # Captura erros de rede ou da API e os imprime no log do servidor
        print(f"Erro ao buscar preço para {symbol} em {url}: {e}")
        raise

# Função para gerar um sinal (sem alterações)
def generate_signal(symbol):
    """Gera um sinal de negociação para um determinado par de moedas."""
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

# Rota principal (sem alterações)
@app.route("/signals")
def get_signals():
    """Endpoint que retorna uma lista de sinais de criptomoedas."""
    try:
        symbols_to_process = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
        signals = [generate_signal(symbol) for symbol in symbols_to_process]
        
        print("Sinais gerados com sucesso via API Binance.US:")
        print(signals)
        return jsonify(signals)
    except Exception as e:
        print(f"Ocorreu um erro geral ao gerar os sinais: {e}")
        return jsonify({"error": f"Falha ao gerar sinais: {str(e)}"}), 500

# Bloco de execução principal (sem alterações)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
