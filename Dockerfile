# ────────────────────────────────────────────────────────────────────────────
# webScrapping — Dockerfile
#
# TIPO DE SERVIÇO: Batch Job (cron / agendado)
#   Este container NÃO é um servidor HTTP de longa duração.
#   Ele executa o ciclo completo de scraping e termina (exit 0).
#   O agendamento deve ser feito externamente via:
#     • Docker: "docker run" chamado pelo cron do host ou pelo CI/CD
#     • Kubernetes: CronJob
#     • Compose: Não use "restart: always" — use "restart: on-failure" ou "no"
# ────────────────────────────────────────────────────────────────────────────

# Imagem base oficial do Python slim — menor footprint
FROM python:3.12-slim

# Evita prompts interativos durante a instalação de pacotes apt
ENV DEBIAN_FRONTEND=noninteractive

# Dependências de sistema exigidas pelo Playwright / Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Bibliotecas gráficas e de fontes para o Chromium headless
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    # Utilitários mínimos
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências Python primeiro (camada de cache separada)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala os browsers do Playwright (apenas o Chromium para economizar espaço)
RUN playwright install chromium --with-deps

# Copia o código-fonte da aplicação
COPY src/ ./src/

# Variáveis de ambiente com valores padrão (sobrescreva via --env-file ou -e)
ENV DB_HOST=localhost \
    DB_PORT=3306 \
    DB_NAME=solarway \
    DB_USER=solarway \
    DB_PASSWORD=

# ─── Execução ───────────────────────────────────────────────────────────────
# O container executa o batch UMA VEZ e termina.
# Para agendar execuções periódicas, use o cron do host ou um Kubernetes CronJob:
#
#   # Exemplo — crontab do host (a cada 6 horas):
#   0 */6 * * * docker run --rm --env-file /opt/solarway/.env solarway/web-scrapping
#
#   # Exemplo — docker compose run (execução avulsa):
#   docker compose run --rm web-scrapping
# ─────────────────────────────────────────────────────────────────────────────
CMD ["python", "-m", "src.main"]
