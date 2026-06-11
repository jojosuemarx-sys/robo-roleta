import os
import requests
import time
from flask import Flask
from threading import Thread

app = Flask(__name__)

# Variável global para armazenar os logs
ultimo_log = "Iniciando monitoramento..."

def motor_leitura():
    global ultimo_log
    while True:
        try:
            url = "https://auto-roulette-vip.p.rapidapi.com/cache/5"
            headers = {
                "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09"),
                "x-rapidapi-host": "auto-roulette-vip.p.rapidapi.com"
            }
            res = requests.get(url, headers=headers, timeout=10)
            status = res.status_code
            conteudo = res.text[:100] # Pega um pedaço para confirmar
            
            ultimo_log = f"Status: {status} | Resposta: {conteudo}"
            print(f"DEBUG: {ultimo_log}")
            
        except Exception as e:
            ultimo_log = f"Erro: {str(e)}"
            print(ultimo_log)
            
        time.sleep(20) # Espera 20 segundos antes da próxima leitura

# Inicia o motor em uma thread separada e persistente
Thread(target=motor_leitura, daemon=True).start()

@app.route('/')
def home():
    return f"<h1>Monitor de Roleta VIP</h1><p>{ultimo_log}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
