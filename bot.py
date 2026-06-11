import os
import requests
import time
import threading
from flask import Flask, render_template_string
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus")
CHAT_ID = "-1003769604348"

historico = []

def motor():
    while True:
        try:
            url = "https://auto-roulette-evolution.p.rapidapi.com/cache/4"
            headers = {"x-rapidapi-key": os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09")}
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            # AQUI ESTÁ A CORREÇÃO:
            # A API retorna data['data'] que é uma lista. Vamos pegar o primeiro item dessa lista.
            novo_num = int(data['data'][0]['result'])
            
            if not historico or historico[-1] != novo_num:
                historico.append(novo_num)
                if len(historico) > 10: historico.pop(0)
                print(f"✅ Número lido com sucesso: {novo_num}")
                
        except Exception as e:
            print(f"⚠️ Erro ao ler API: {e}")
            
        time.sleep(20)

@app.route('/')
def home():
    ultimo = historico[-1] if historico else 'Aguardando...'
    return f"<h1>Robô Online</h1><p>Último número lido: {ultimo}</p><p>Histórico: {historico}</p>"

if __name__ == "__main__":
    threading.Thread(target=motor, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
