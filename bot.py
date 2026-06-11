import os
import requests
import time
import threading
from flask import Flask, render_template_string
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus")
historico = []

def motor():
    print("--- MOTOR INICIADO ---")
    while True:
        try:
            url = "https://auto-roulette-vip.p.rapidapi.com/cache/5"
            headers = {
                "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09"),
                "x-rapidapi-host": "auto-roulette-vip.p.rapidapi.com"
            }
            res = requests.get(url, headers=headers, timeout=10).json()
            
            # DIAGNÓSTICO: Vou imprimir a resposta bruta no log
            print(f"DEBUG API: {res}")
            
            if 'data' in res and len(res['data']) > 0:
                novo_num = int(res['data'][0]['result'])
                if not historico or historico[-1] != novo_num:
                    historico.append(novo_num)
                    if len(historico) > 20: historico.pop(0)
                    print(f"✅ NOVO NÚMERO: {novo_num}")
            else:
                print("⚠️ API retornou dados vazios.")
                
        except Exception as e:
            print(f"⚠️ Erro no motor: {e}")
            
        time.sleep(15)

threading.Thread(target=motor, daemon=True).start()

@app.route('/')
def home():
    return render_template_string("<h1>Robô Online</h1><p>Último: {{ historico[-1] if historico else 'Aguardando...' }}</p>", historico=historico)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
