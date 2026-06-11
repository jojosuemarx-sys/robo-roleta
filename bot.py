import os
import requests
import time
import threading
from flask import Flask

app = Flask(__name__)

# --- DIAGNÓSTICO ---
def motor():
    while True:
        try:
            url = "https://auto-roulette-vip.p.rapidapi.com/cache/5"
            headers = {
                "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09"),
                "x-rapidapi-host": "auto-roulette-vip.p.rapidapi.com"
            }
            res = requests.get(url, headers=headers, timeout=10)
            
            # Printa tudo no Log do Render para a gente ver o que está acontecendo
            print(f"DEBUG: Status Code: {res.status_code}")
            print(f"DEBUG: Resposta completa: {res.text}")
            
        except Exception as e:
            print(f"DEBUG: Erro de conexão: {e}")
            
        time.sleep(30)

@app.route('/')
def home():
    return "Monitorando logs no Render..."

if __name__ == "__main__":
    threading.Thread(target=motor, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
