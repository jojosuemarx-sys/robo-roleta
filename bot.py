import os
import requests
import time
from flask import Flask
from threading import Thread

app = Flask(__name__)

# --- MOTOR DE LEITURA ROBUSTO ---
def rodar_motor():
    print("--- MOTOR INICIANDO TENTATIVA DE LEITURA ---")
    while True:
        try:
            url = "https://auto-roulette-vip.p.rapidapi.com/cache/5"
            headers = {
                "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09"),
                "x-rapidapi-host": "auto-roulette-vip.p.rapidapi.com"
            }
            # Faz a requisição
            response = requests.get(url, headers=headers, timeout=15)
            
            # Imprime tudo no log para vermos o que está acontecendo
            print(f"DEBUG: Status={response.status_code} | Resposta={response.text[:100]}")
            
        except Exception as e:
            print(f"DEBUG: Erro ao conectar: {e}")
            
        time.sleep(30) # Aguarda 30 segundos

# Inicia o motor ANTES de rodar o app
Thread(target=rodar_motor, daemon=True).start()

@app.route('/')
def home():
    return "O robô está rodando. Verifique o LOG do Render para ver a resposta da API."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
