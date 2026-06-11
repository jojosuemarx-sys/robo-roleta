# Usa a imagem base do Playwright
FROM mcr.microsoft.com/playwright:v1.44.0-jammy

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos para o container
COPY . .

# Instala as dependências a partir do requirements.txt
# (Isso garante que o pyTelegramBotAPI seja instalado)
RUN pip3 install --no-cache-dir -r requirements.txt && \
    playwright install chromium

# Comando para rodar o bot diretamente
CMD ["python3", "bot.py"]
