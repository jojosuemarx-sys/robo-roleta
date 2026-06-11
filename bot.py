import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

app = Flask('')

# CONFIGURAÇÕES
TOKEN = "8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus"
CHAT_ID = "-1003769604348"
URL = "https://tipminer.com/br/historico/evolution/roleta-ao-vivo"

# Variável para evitar repetição de sinal
ultimo_numero_processado = None

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def monitorar():
    global ultimo_numero_processado
    print("🤖 Robô Autônomo Iniciado via TipMiner!")
    
    while True:
        try:
            # 1. Acessa o TipMiner
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(URL, headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # 2. Captura os números (A classe 'round-number' do TipMiner)
            numeros = [int(div.text) for div in soup.find_all('div', class_='round-number') if div.text.isdigit()]
            
            # 3. Verifica se tem dado novo
            if numeros and numeros[0] != ultimo_numero_processado:
                ultimo_numero_processado = numeros[0]
                print(f"🎰 Novo giro detectado: {ultimo_numero_processado}")
                
                # AQUI você insere sua lógica de envio
                # Exemplo: enviar_telegram(f"Novo giro: {ultimo_numero_processado}")
                
        except Exception as e:
            print(f"Erro na leitura: {e}")
            
        time.sleep(20) # Intervalo seguro

@app.route('/')
def home():
    return "🤖 O Analista Assertivo está 100% Autônomo via TipMiner!"

if __name__ == "__main__":
    Thread(target=monitorar, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
