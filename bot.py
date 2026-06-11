import os
import requests
from flask import Flask

app = Flask(__name__)

# --- CONFIGURAÇÃO ---
# Se a chave não estiver no Render, ele usa esta que você me passou
RAPID_KEY = os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09")

@app.route('/')
def home():
    try:
        # Tenta conectar na API
        url = "https://auto-roulette-evolution.p.rapidapi.com/cache/4"
        headers = {
            "x-rapidapi-key": RAPID_KEY,
            "x-rapidapi-host": "auto-roulette-evolution.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # Exibe o que aconteceu na tela
        if response.status_code == 200:
            return f"✅ API FUNCIONANDO! Resposta: {response.text}"
        else:
            return f"❌ ERRO NA API: Código {response.status_code}. Resposta: {response.text}"
            
    except Exception as e:
        return f"❌ ERRO DE CONEXÃO: {str(e)}"

if __name__ == "__main__":
    # Roda o servidor
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
