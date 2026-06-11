import os
import time
import requests
import random
from flask import Flask
from threading import Thread

app = Flask('')

TOKEN = "8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus"
CHAT_ID = "-1003769604348"
# Usando a versão mobile do site, que costuma ser menos protegida
URL = "https://m.tipminer.com/br/historico/evolution/roleta-ao-vivo"

# Lista de User-Agents para variar e enganar o bloqueio
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"
]

def enviar_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def monitorar():
    print("🤖 Robô em modo 'Stealth' iniciado!")
    while True:
        try:
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            # O truque aqui é usar um timeout curto e variar o User-Agent
            r = requests.get(URL, headers=headers, timeout=15)
            
            if r.status_code == 200:
                print("✅ Conexão estabelecida com sucesso.")
            else:
                print(f"⚠️ Acesso limitado. Status: {r.status_code}")
                
        except Exception as e:
            print(f"Erro de rede: {e}")
            
        time.sleep(60) # Aumentamos o tempo para evitar banimento do IP do Render

@app.route('/')
def home():
    return "Bot Online"

if __name__ == "__main__":
    Thread(target=monitorar, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
