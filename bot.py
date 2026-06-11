import os
import requests
import time
import threading
from flask import Flask, render_template_string
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus")
CHAT_ID = "-1003769604348"

# Variáveis do robô
historico = []
aposta_ativa = None # Armazena o sinal que o bot enviou para conferir depois

def analisar_e_enviar():
    if len(historico) < 3: return
    
    # Pega os últimos 3 números
    ultimos = [int(n) for n in historico[-3:]]
    
    # Lógica de Cores (Exemplo: 3 Pretos -> Entra no Vermelho)
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cores = ["🔴" if n in vermelhos else "⚫️" for n in ultimos]
    
    if cores == ["⚫️", "⚫️", "⚫️"]:
        sinal = "🔴 VERMELHO"
        bot.send_message(CHAT_ID, f"🚨 SINAL: Apostar no {sinal}. Proteção no Zero.")
        global aposta_ativa
        aposta_ativa = {"tipo": "cor", "alvo": "vermelho", "gale": 0}

def motor():
    global aposta_ativa
    while True:
        try:
            url = "https://auto-roulette-evolution.p.rapidapi.com/cache/4"
            headers = {"x-rapidapi-key": os.environ.get("RAPIDAPI_KEY", "d76bfabe1dmsh4cf05a08aa6bd87p18eac2jsn84a37e3beb09")}
            data = requests.get(url, headers=headers).json()
            
            # Extraindo o número do formato que você me mostrou
            novo_num = int(data['data'][0]['result'])
            
            if not historico or historico[-1] != novo_num:
                historico.append(novo_num)
                # Se tiver aposta ativa, confere o resultado
                if aposta_ativa:
                    # Lógica simples de conferência (você pode expandir aqui)
                    bot.send_message(CHAT_ID, f"🎯 O número saiu: {novo_num}. Conferindo resultado...")
                    aposta_ativa = None
                
                analisar_e_enviar()
        except:
            pass
        time.sleep(30)

@app.route('/')
def home():
    return f"<h1>Robô Online</h1><p>Último número: {historico[-1] if historico else 'Aguardando...'}</p>"

if __name__ == "__main__":
    threading.Thread(target=motor, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
