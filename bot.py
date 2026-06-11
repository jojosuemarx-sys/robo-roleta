import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

# === CONFIGURAÇÕES ===
TOKEN = "8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus"
CHAT_ID = "-1003769604348"
URL_TIPMINER = "https://tipminer.com/br/historico/evolution/roleta-ao-vivo"
VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

app = Flask('')

# === FUNÇÕES DE APOIO ===
def obter_cor(numero):
    if numero == 0: return "ZERO"
    return "VERMELHO" if numero in VERMELHOS else "PRETO"

def obter_coluna(numero):
    if numero == 0: return 0
    if numero in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]: return 1
    if numero in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]: return 2
    return 3

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Erro Telegram: {e}")

# === LÓGICA DE ANÁLISE ===
def analisar_dados(historico):
    print(f"📊 Analisando: {historico[:10]}")
    
    # 🎨 Cores
    cores = [obter_cor(n) for n in historico if obter_cor(n) != "ZERO"]
    if cores:
        cor_atual, seq = cores[0], 0
        for c in cores:
            if c == cor_atual: seq += 1
            else: break
        
        if seq in [2, 3, 4, 5]:
            cor_oposta = "PRETO" if cor_atual == "VERMELHO" else "VERMELHO"
            tipo = "🚨 SINAL" if seq >= 3 else "👀 PRE-ALERTA"
            msg = f"{tipo}: Apostar no {cor_oposta} (Sequência de {seq} em {cor_atual})"
            enviar_telegram(msg)

    # 📊 Colunas
    for col in [1, 2, 3]:
        ausencia = 0
        for n in historico:
            if n == 0: ausencia += 1; continue
            if obter_coluna(n) != col: ausencia += 1
            else: break
        
        if ausencia in [2, 3, 4, 5]:
            tipo = "🚨 SINAL" if ausencia >= 3 else "👀 PRE-ALERTA"
            msg = f"{tipo}: Coluna {col} está há {ausencia} rodadas sem sair."
            enviar_telegram(msg)

# === MOTOR DE LEITURA (AUTÔNOMO) ===
def monitorar():
    ultimo_historico = []
    print("🤖 Robô Autônomo Iniciado!")
    
    while True:
        try:
            r = requests.get(URL_TIPMINER, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            numeros = [int(div.text) for div in soup.find_all('div', class_='round-number') if div.text.isdigit()]
            
            if numeros and numeros != ultimo_historico:
                ultimo_historico = numeros
                analisar_dados(numeros)
        except Exception as e:
            print(f"Erro na leitura: {e}")
            
        time.sleep(20)

@app.route('/')
def home():
    return "🤖 Sistema de Análise Autônomo Online."

if __name__ == "__main__":
    Thread(target=monitorar, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
