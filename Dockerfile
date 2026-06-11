# Usa a imagem base do Playwright
FROM mcr.microsoft.com/playwright:v1.44.0-jammy

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Atualiza o gerenciador de pacotes e instala as dependências usando pip3
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install --no-cache-dir flask requests playwright gunicorn && \
    playwright install chromium

# Comando para rodar a aplicação
CMD ["gunicorn", "bot:app", "--bind", "0.0.0.0:10000"]
