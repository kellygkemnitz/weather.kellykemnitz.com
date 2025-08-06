FROM python:3.12-slim

WORKDIR /app

RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --upgrade pip

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY modules/ modules/
COPY static/ static/
COPY templates/ templates/
COPY .env .
COPY app.py .
COPY scraper.py .

EXPOSE 8081

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8001", "app:app"]
