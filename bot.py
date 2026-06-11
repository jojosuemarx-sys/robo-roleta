import os
import requests
import time
import threading
from flask import Flask, render_template_string
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus")
historico = []

# --- MOTOR DE LEITURA ---
def motor():
    while True:
        try:
            url = "https://auto-roulette-vip.p.rapidapi.com/cache/5"
            headers = {
                "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09"),
                "x-rapidapi-host": "auto-roulette-vip.p.rapidapi.com"
            }
            res = requests.get(url, headers=headers, timeout=10).json()
            novo_num = int(res['data'][0]['result'])
            
            if not historico or historico[-1] != novo_num:
                historico.append(novo_num)
                if len(historico) > 20: historico.pop(0) # Mantém os últimos 20
        except:
            pass
        time.sleep(5) # Lê a cada 5 segundos para não sobrecarregar

# --- INTERFACE BONITINHA ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="2">
    <style>
        body { background: #0f172a; color: white; font-family: 'Arial', sans-serif; text-align: center; padding: 50px; }
        .bola { display: inline-block; width: 50px; height: 50px; line-height: 50px; border-radius: 50%; 
                background: #1e293b; margin: 5px; font-weight: bold; border: 2px solid #38bdf8; }
        .titulo { color: #38bdf8; font-size: 2.5em; margin-bottom: 20px; }
        .container { background: #1e293b; padding: 30px; border-radius: 15px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="titulo">Mesa VIP em Tempo Real</h1>
        <p>Último número sorteado:</p>
        <div class="bola" style="font-size: 24px; background: #38bdf8; color: black;">{{ historico[-1] if historico else '-' }}</div>
        <br><br>
        <p>Histórico recente:</p>
        <div>
            {% for n in historico|reverse %}
                <span class="bola">{{ n }}</span>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, historico=historico)

if __name__ == "__main__":
    threading.Thread(target=motor, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get
