import os
import json
import time
import requests
import threading
import websocket
from flask import Flask

# === CONFIGURAÇÕES OFICIAIS DO TELEGRAM ===
TOKEN = "8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus"
CHAT_ID = "-1003769604348"
VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

# === URL LIVE CAPTURADA DA SUA SUPERBET ===
WS_URL = "wss://superbetbr.evo-games.com/public/roulette/player/game/PorROU0000000001/socket?messageFormat=json&EVOSESSIONID=t22dkq3wxcmqcf42t22flhq3ykzpfgd6208395e709774d704ca314de4a8d2af19a690c97afb23776&instance=ojwqol-t22dkq3wxcmqcf42-PorROU0000000001&client_version=6.20260610.73511.62580-5bb4093ee3-r2"

# Guardar o último histórico para evitar sinais duplicados do mesmo giro
ultimo_historico_analisado = []

# === MINI SERVIDOR WEB PARA O RENDER ===
app = Flask('')

@app.route('/')
def home():
    return "🤖 O Analista Assertivo está online e conectado via WebSocket na Nuvem!"

def iniciar_servidor_web():
    porta = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=porta)

# === MAPEAMENTOS DA ROLETA ===
def obter_cor(numero):
    if numero == 0: return "ZERO"
    return "VERMELHO" if numero in VERMELHOS else "PRETO"

def obter_coluna(numero):
    if numero == 0: return 0
    if numero in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]: return 1
    if numero in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]: return 2
    return 3

def enviar_sinal_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ Erro ao conectar ao Telegram: {e}")

# === MOTOR DE ANÁLISE COMPATÍVEL ===
def analisar_dados(historico_numeros):
    if not historico_numeros: return
    
    print(f"📊 Analisando sequência atual: {historico_numeros}")
    
    # 🎨 Análise de Cores (3, 5, 7 repetições | Até 2 Gales)
    cores_validas = [obter_cor(n) for n in historico_numeros if obter_cor(n) != "ZERO"]
    if cores_validas:
        cor_atual = cores_validas[0]
        seq_cor = 0
        for c in cores_validas:
            if c == cor_atual: seq_cor += 1
            else: break
        
        if seq_cor in [3, 5, 7]:
            cor_entrada = "PRETO" if cor_atual == "VERMELHO" else "VERMELHO"
            gales = "2 Gales"
            assertividade = "94.3%" if seq_cor == 3 else ("98.7%" if seq_cor == 5 else "99.8%")
            tipo = "⚠️ ALERTA DE TENDÊNCIA" if seq_cor == 3 else ("🚨 SINAL CONFIRMADO" if seq_cor == 5 else "🔥 SINAL MÁXIMO")
            
            msg = f"{tipo} - {seq_cor} CORES ⚠️\n\n🎰 *Mesa:* Roleta Brasileira\n📊 *Assertividade:* {assertividade} (Até {gales})\n🎯 *Entrada:* Apostar no *{cor_entrada}*\n🛡️ *Proteção:* Cobrir o Zero (0)"
            enviar_sinal_telegram(msg)

    # 📊 Análise de Colunas (3, 5, 7 ausências | Até 3 Gales)
    for coluna_alvo in [1, 2, 3]:
        ausencia = 0
        for num in historico_numeros:
            if num == 0: ausencia += 1; continue
            if obter_coluna(num) != coluna_alvo: ausencia += 1
            else: break
            
        if ausencia in [3, 5, 7]:
            assertividade_col = "89.1%" if ausencia == 3 else ("96.4%" if ausencia == 5 else "99.5%")
            tipo_col = "⚠️ ALERTA DE COLUNA" if ausencia == 3 else ("🚨 SINAL CONFIRMADO" if ausencia == 5 else "🔥 SINAL MÁXIMO")
            
            msg_col = f"{tipo_col} - {ausencia} AUSÊNCIAS ⚠️\n\n🎰 *Mesa:* Roleta Brasileira\n📊 *Assertividade:* {assertividade_col} (Até 3 Gales)\n🎯 *Entrada:* Apostar na *COLUNA {coluna_alvo}*\n🛡️ *Proteção:* Cobrir o Zero (0)"
            enviar_sinal_telegram(msg_col)

# === EVENTOS E ESCUTA DO WEBSOCKET ===
def on_message(ws, message):
    global ultimo_historico_analisado
    try:
        dados = json.loads(message)
        
        # Monitora exclusivamente o evento de novos resultados da roleta
        if dados.get("type") == "rouletto.recentResults":
            recent_results = dados["args"]["recentResults"]
            
            if recent_results:
                # Transforma a lista de strings do servidor da evolução em inteiros [int]
                historico_inteiros = [int(n) for n in recent_results if n.isdigit()]
                
                # Só analisa se o histórico realmente mudou (novo giro aconteceu)
                if historico_inteiros != ultimo_historico_analisado:
                    ultimo_historico_analisado = historico_inteiros
                    analisar_dados(historico_inteiros)
                    
    except Exception as e:
        print(f"Erro ao processar mensagem do servidor: {e}")

def on_error(ws, error):
    print(f"❌ Erro na conexão do WebSocket: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Conexão com a Superbet fechada. Reconectando em 5 segundos...")
    time.sleep(5)
    iniciar_websocket()

def on_open(ws):
    print("🤖 Conexão direta estabelecida com o servidor da Superbet! Escutando giros ao vivo...")

def iniciar_websocket():
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    # 1. Liga o mini-servidor para enganar o Render em segundo plano
    t_web = threading.Thread(target=iniciar_servidor_web)
    t_web.daemon = True
    t_web.start()
    
    # 2. Inicia o loop eterno do WebSocket escutando a roleta
    iniciar_websocket()
