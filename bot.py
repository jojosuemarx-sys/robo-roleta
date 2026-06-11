import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask('')

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
# URL de API interna que o próprio site utiliza para buscar os resultados
URL_API = "https://tipminer.com/api/v1/evolution/roleta-ao-vivo/history"

def enviar_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
    except: pass

def monitorar():
    print("🤖 Monitor de API Ativado!")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://tipminer.com/br/historico/evolution/roleta-ao-vivo"
    }
    
    ultimo_id = None
    
    while True:
        try:
            r = requests.get(URL_API, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                # Acessa o primeiro item da lista de resultados
                if data and len(data) > 0:
                    giro = data[0]
                    numero = giro.get("number")
                    giro_id = giro.get("id")
                    
                    if giro_id != ultimo_id:
                        ultimo_id = giro_id
                        msg = f"🎰 <b>Novo Giro:</b> {numero}"
                        enviar_telegram(msg)
                        print(f"✅ Giro detectado: {numero} (ID: {giro_id})")
            else:
                print(f"⚠️ API retornou status {r.status_code}")
                
        except Exception as e:
            print(f"Erro na API: {e}")
            
        time.sleep(20)

@app.route('/')
def home():
    return "Bot de API Online"

if __name__ == "__main__":
    Thread(target=monitorar, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))                elementos = soup.select('.ball')
                
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
