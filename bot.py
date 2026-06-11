import os
import telebot
from flask import Flask
from playwright.sync_api import sync_playwright
import threading
import time

app = Flask(__name__)
bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))
CHAT_ID = "1558589953"

@app.route('/')
def home():
    return "Bot de Monitoramento Ativo!"

def monitorar():
    with sync_playwright() as p:
        # Adicionando um User-Agent para parecer um navegador real
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        page = context.new_page()
        
        page.goto("https://tipminer.com/br/historico/evolution/vip-auto-roulette")
        
        last_number = ""
        
        while True:
            try:
                # Aguarda o elemento aparecer na tela (timeout de 10s)
                page.wait_for_selector(".cell_result", timeout=10000)
                resultado = page.query_selector(".cell_result").inner_text()
                
                if resultado and resultado != last_number:
                    last_number = resultado
                    mensagem = f"🎯 Novo número na roleta: {last_number}"
                    bot.send_message(CHAT_ID, mensagem)
                    print(mensagem)
                    
            except Exception as e:
                print(f"Buscando... (Erro: {e})")
                # Se der erro, recarrega a página para tentar recuperar
                page.reload()
            
            time.sleep(5)

threading.Thread(target=monitorar, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
