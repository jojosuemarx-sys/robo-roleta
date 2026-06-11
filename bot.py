import os
import requests
import time
from flask import Flask, render_template_string

app = Flask(__name__)

# --- TESTE FORÇADO DE LEITURA ---
def ler_api():
    try:
        url = "https://auto-roulette-vip.p.rapidapi.com/cache/5"
        headers = {
            "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09"),
            "x-rapidapi-host": "auto-roulette-vip.p.rapidapi.com"
        }
        res = requests.get(url, headers=headers, timeout=10)
        print(f"DEBUG_API_STATUS: {res.status_code}")
        print(f"DEBUG_API_TEXT: {res.text[:200]}") # Imprime os primeiros 200 caracteres
    except Exception as e:
        print(f"ERRO_CRITICO: {e}")

@app.route('/')
def home():
    ler_api() # Lê a cada vez que alguém abre o seu site
    return "<h1>Monitorando... verifique o log do Render agora!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
