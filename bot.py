import os
from flask import Flask, render_template_string
import telebot

app = Flask(__name__)

# --- SUAS CREDENCIAIS ---
# ATENÇÃO: Se for subir para o GitHub público, outras pessoas poderão ver sua chave.
TOKEN = "8730429065:AAGq1CORU8-uVeseK06DxmuRhSbEqU77jus"
CHAT_ID = "-1003769604348"

bot = telebot.TeleBot(TOKEN)

# Design da página web com o botão de teste
HTML_PAGINA = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel do Analisador</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0e1621;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background-color: #17212b;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            max-width: 400px;
            width: 100%;
        }
        h2 { margin-bottom: 10px; color: #2481cc; }
        p { color: #7f92a4; font-size: 14px; margin-bottom: 30px; }
        button {
            background-color: #2481cc;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
            width: 100%;
        }
        button:hover { background-color: #2996e6; }
        button:active { transform: scale(0.98); }
        .status {
            margin-top: 20px;
            padding: 10px;
            border-radius: 6px;
            font-size: 14px;
        }
        .sucesso { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; }
        .erro { background-color: rgba(231, 76, 60, 0.2); color: #e74c3c; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Analisador de Roleta</h2>
        <p>Clique no botão para testar o disparo de alertas no Telegram.</p>
        
        <form action="/disparar" method="POST">
            <button type="submit">🚀 TESTAR DISPARO</button>
        </form>

        {% if status == 'sucesso' %}
            <div class="status sucesso">✅ O analisador assertivo, 24h analisando! Mensagem enviada.</div>
        {% elif status == 'erro' %}
            <div class="status erro">❌ Erro ao enviar: {{ erro_msg }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGINA)

@app.route('/disparar', methods=['POST'])
def disparar_mensagem():
    try:
        # Texto exato que será enviado no seu canal/grupo
        texto_sinal = (
            "🤖 **O analisador assertivo, 24h analisando!** 🚀\n\n"
            "🎯 O sistema de monitoramento está operando com sucesso."
        )
        
        # Envia diretamente para o seu Canal/Grupo
        bot.send_message(CHAT_ID, texto_sinal, parse_mode='Markdown')
        return render_template_string(HTML_PAGINA, status='sucesso')
        
    except Exception as e:
        return render_template_string(HTML_PAGINA, status='erro', erro_msg=str(e))

if __name__ == "__main__":
    # Roda o servidor web na porta local 5000 (ou na porta que o Render definir)
    porta = int(os.environ.get("PORT", 5000))
    print(f"🌐 Servidor rodando! Acesse: http://localhost:{porta}")
    app.run(host='0.0.0.0', port=porta)
