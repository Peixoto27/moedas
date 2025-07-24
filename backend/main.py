import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests

# Inicializa a aplicação Flask
app = Flask(__name__)

# Habilita o CORS
CORS(app)

# --- FUNÇÃO ALTERADA COM PROXY ---
def get_crypto_price(symbol):
    """Busca o preço atual de um par de moedas na Binance usando um proxy para evitar bloqueio geográfico."""
    
    # URL original da API da Binance
    target_url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    
    # Usaremos um proxy para fazer a chamada.
    # Este é um proxy público que pode ser lento ou falhar, mas serve para contornar o bloqueio.
    # O proxy pega na nossa URL alvo e acede-a por nós.
    proxy_url = f'https://api.allorigins.win/get?url={target_url}'
    
    try:
        # O pedido agora é feito ao servidor proxy
        response = requests.get(proxy_url )
        response.raise_for_status()
        
        # O proxy envolve a resposta original da Binance dentro de outro JSON.
        # Precisamos de extrair o conteúdo original.
        proxy_data = response.json()
        
        # O conteúdo real da Binance está na chave 'contents'
        import json
        binance_data = json.loads(proxy_data['contents'])
        
        # Verificamos se a Binance devolveu um erro dentro do JSON
        if 'code' in binance_data and 'msg' in binance_data:
            raise Exception(f"Erro da API Binance: {binance_data['msg']}")
            
        return float(binance_data['price'])
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao contactar o proxy ou a API para {symbol}: {e}")
        raise
    except Exception as e:
        print(f"Erro ao processar a resposta do proxy para {symbol}: {e}")
        raise

# Função para gerar um sinal (sem alterações)
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

# Rota principal (sem alterações)
@app.route("/signals")
def get_signals():
    try:
        symbols_to_process = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
        signals = [generate_signal(symbol) for symbol in symbols_to_process]
        print("Sinais gerados com sucesso via proxy:")
        print(signals)
        return jsonify(signals)
    except Exception as e:
        print(f"Ocorreu um erro geral ao gerar os sinais: {e}")
        return jsonify({"error": f"Falha ao gerar sinais: {str(e)}"}), 500

# Bloco de execução principal (sem alterações)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
