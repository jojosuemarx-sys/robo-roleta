import requests
from flask import Flask
import threading
import time

app = Flask(__name__)

def testar_conexao():
    print("--- TESTANDO CONEXÃO EXTERNA ---")
    try:
        # Vamos tentar conectar no Google primeiro para ver se o Render permite acesso externo
        res = requests.get("https://www.google.com", timeout=10)
        print(f"DEBUG: Conexão Google - Status: {res.status_code}")
        
        # Agora tentamos a roleta
        url = "https://auto-roulette-vip.p.rapidapi.com/cache/5"
        headers = {"x-rapidapi-key": "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09"}
        res2 = requests.get(url, headers=headers, timeout=15)
        print(f"DEBUG: Conexão Roleta - Status: {res2.status_code} | Resposta: {res2.text[:100]}")
        
    except Exception as e:
        print(f"DEBUG: Erro na conexão: {e}")

threading.Thread(target=testar_conexao, daemon=True).start()

@app.route('/')
def index():
    return "Testando..."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
