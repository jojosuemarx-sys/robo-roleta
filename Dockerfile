FROM mcr.microsoft.com/playwright:v1.44.0-jammy
WORKDIR /app
COPY . .
RUN pip install flask requests playwright
# Garante que o navegador seja instalado
RUN playwright install chromium
CMD ["gunicorn", "bot:app", "--bind", "0.0.0.0:10000"]
