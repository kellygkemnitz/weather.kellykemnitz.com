FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

COPY --from=builder /install /usr/local

COPY modules/ modules/
COPY static/ static/
COPY templates/ templates/
COPY app.py .
COPY scraper.py .

ENV STATION=""
ENV FREQ=""
ENV ATTEMPTS=""
ENV WAIT_TIME=""

RUN useradd -m appuser
USER appuser

EXPOSE 8001

CMD ["gunicorn", "-w", "1", "-k", "gthread", "--threads", "4", "--max-requests", "200", "--max-requests-jitter", "50", "-b", "0.0.0.0:8001", "app:app"]
