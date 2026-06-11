import os
from flask import Flask
from playwright.sync_api import sync_playwright
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Sinais Online!"

def monitorar_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Navegador iniciado no Render...")

        while True:
            try:
                # Substitua pela URL do site e o seletor CSS do número
                page.goto("URL_DO_SITE_AQUI")
                texto = page.inner_text("SELETOR_CSS_AQUI")
                print(f"Número lido: {texto}")
            except Exception as e:
                print(f"Erro na leitura: {e}")
            time.sleep(30)

# Inicia a thread
threading.Thread(target=monitorar_site, daemon=True).start()

if __name__ == "__main__":
    app.run()
