import os
import time
import requests
from flask import Flask
from threading import Thread
from bs4 import BeautifulSoup

app = Flask('')

# Configurações do Railway
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL = "https://tipminer.com/br/historico/evolution/roleta-ao-vivo"

def enviar_telegram(msg):
    try:
        url_api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url_api, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
    except: pass

def monitorar():
    print("🤖 Robô de Análise em Execução!")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    ultimo_numero = ""
    
    while True:
        try:
            r = requests.get(URL, headers=headers, timeout=15)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Esta parte busca o último número da roleta baseado na estrutura do site
                # O seletor '.ball' é comum no TipMiner para identificar os números
                elementos = soup.select('.ball')
                
                if elementos:
                    novo_numero = elementos[0].text.strip()
                    
                    if novo_numero != ultimo_numero:
                        ultimo_numero = novo_numero
                        msg = f"🎰 <b>Novo Número:</b> {novo_numero}"
                        enviar_telegram(msg)
                        print(f"✅ Giro detectado: {novo_numero}")
            else:
                print(f"⚠️ Acesso bloqueado (Status {r.status_code})")
                
        except Exception as e:
            print(f"Erro na análise: {e}")
            
        time.sleep(30) # Monitora a cada 30 segundos

@app.route('/')
def home():
    return "Bot de análise online"

if __name__ == "__main__":
    Thread(target=monitorar, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
