import os
import time
import threading
import requests
from flask import Flask, render_template_string
import telebot

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
TOKEN = "8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus"
CHAT_ID = "-1003769604348"
RAPID_KEY = os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09")
bot = telebot.TeleBot(TOKEN)

# Armazena os últimos 5 números
historico = []

def loop_monitoramento():
    while True:
        try:
            url = "https://auto-roulette-evolution.p.rapidapi.com/cache/4"
            headers = {"x-rapidapi-key": RAPID_KEY, "x-rapidapi-host": "auto-roulette-evolution.p.rapidapi.com"}
            res = requests.get(url, headers=headers).json()
            
            # Ajuste simples para pegar o primeiro número
            novo_num = int(res[0])
            if not historico or historico[-1] != novo_num:
                historico.append(novo_num)
                if len(historico) > 5: historico.pop(0)
        except:
            pass
        time.sleep(30)

# --- INTERFACE WEB ---
HTML_PAINEL = """
<!DOCTYPE html>
<html>
<head>
    <title>Painel do Robô</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body { font-family: sans-serif; background: #121212; color: white; text-align: center; padding: 20px; }
        .bola { font-size: 30px; margin: 10px; display: inline-block; padding: 15px; border-radius: 50%; background: #333; }
        button { padding: 15px 30px; font-size: 18px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Painel de Controle</h1>
    <p>Últimos números lidos:</p>
    <div>{% for n in historico %}<span class="bola">{{ n }}</span>{% endfor %}</div>
    <br><br>
    <form action="/testar" method="post">
        <button type="submit">ENVIAR MENSAGEM DE TESTE</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAINEL, historico=historico)

@app.route('/testar', methods=['POST'])
def testar():
    bot.send_message(CHAT_ID, "🤖 Bot operando normalmente! Mensagem de teste enviada.")
    return "Mensagem enviada com sucesso! <a href='/'>Voltar</a>"

if __name__ == "__main__":
    threading.Thread(target=loop_monitoramento, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
