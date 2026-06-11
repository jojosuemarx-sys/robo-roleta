import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask('')

# CONFIGURAÇÕES
TOKEN = "8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus"
CHAT_ID = "-1003769604348"
# Esta é a URL da API que o TipMiner consulta para obter os dados
API_URL = "https://tipminer.com/api/v2/evolution/roulette/history?limit=20"

VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
ultimo_id_processado = None

def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def analisar_estrategia(historico):
    # Logica simplificada de cores para exemplo
    if not historico: return
    
    ultimo = historico[0]
    cor = "VERMELHO" if ultimo in VERMELHOS else "PRETO"
    
    # Exemplo de envio de teste
    msg = f"🎰 *Último giro:* {ultimo} ({cor})"
    enviar_telegram(msg)

def monitorar():
    global ultimo_id_processado
    print("🤖 Robô Autônomo via API iniciado!")
    
    while True:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            # Faz a requisição direta para a API de dados
            r = requests.get(API_URL, headers=headers, timeout=10)
            dados = r.json()
            
            # Pega o primeiro item da lista de resultados
            if dados and 'data' in dados:
                resultado_atual = dados['data'][0]
                numero = resultado_atual['number']
                id_rodada = resultado_atual['id']
                
                if id_rodada != ultimo_id_processado:
                    ultimo_id_processado = id_rodada
                    print(f"🎰 Novo giro detectado: {numero}")
                    analisar_estrategia([numero])
        except Exception as e:
            print(f"Erro de leitura: {e}")
            
        time.sleep(15)

@app.route('/')
def home():
    return "🤖 Sistema de Análise Autônomo Online."

if __name__ == "__main__":
    Thread(target=monitorar, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
