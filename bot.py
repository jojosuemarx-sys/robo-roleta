import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask('')

# URL de um Proxy gratuito para tentar burlar o bloqueio
# Em produção, proxies gratuitos caem muito, mas serve para testar
PROXIES = {
    'http': 'http://185.162.229.185:80', 
    'https': 'http://185.162.229.185:80'
}

def monitorar():
    print("🤖 Robô com Proxy iniciado!")
    while True:
        try:
            # Tenta acessar via Proxy
            r = requests.get("https://tipminer.com/br/historico/evolution/roleta-ao-vivo", 
                             proxies=PROXIES, timeout=10)
            
            if r.status_code == 200:
                print("✅ Acesso via Proxy funcionando!")
            else:
                print(f"❌ Proxy falhou com status {r.status_code}")
                
        except Exception as e:
            print(f"Erro de conexão: {e}")
        time.sleep(60)

@app.route('/')
def home():
    return "Bot Online"

if __name__ == "__main__":
    Thread(target=monitorar, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
