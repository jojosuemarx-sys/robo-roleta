import os
import time
import threading
import requests
from flask import Flask, render_template_string
import telebot

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-1003769604348")
RAPID_KEY = os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09")
bot = telebot.TeleBot(TOKEN)

historico = []

def classificar_aposta(n):
    cor = "🔴" if n in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "⚫️"
    if n == 0: cor = "🟢"
    duzia = "1ª Dúzia" if 1<=n<=12 else "2ª Dúzia" if 13<=n<=24 else "3ª Dúzia"
    coluna = "1ª Coluna" if n%3==1 else "2ª Coluna" if n%3==2 else "3ª Coluna"
    return {"cor": cor, "duzia": duzia, "coluna": coluna}

def loop_monitoramento():
    while True:
        try:
            url = "https://auto-roulette-evolution.p.rapidapi.com/cache/4"
            headers = {"x-rapidapi-key": RAPID_KEY, "x-rapidapi-host": "auto-roulette-evolution.p.rapidapi.com"}
            res = requests.get(url, headers=headers).json()
            
            # Tenta pegar o número (ajuste conforme o teste que você fizer depois)
            novo_num = int(res[0])
            
            if not historico or historico[-1] != novo_num:
                historico.append(novo_num)
                if len(historico) > 10: historico.pop(0)
                print(f"Número lido: {novo_num}")
                
        except Exception as e:
            print(f"Erro na API: {e}")
        time.sleep(20)

@app.route('/')
def home():
    return "Bot de Análise 24h Online!"

if __name__ == "__main__":
    threading.Thread(target=loop_monitoramento, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
