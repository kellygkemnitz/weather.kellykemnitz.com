FROM python:3.12-slim

WORKDIR /app

RUN python -m venv /opt/venv

SHELL ["/bin/bash", "-c"]
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache -Ur requirements.txt

COPY assets .
COPY dash_app.py plotly_graphs.py scrape_wunderground.py .
COPY README.md .
COPY settings.yaml .

CMD ["gunicorn", "-b", "0.0.0.0:8001", "-w", "1", "-k", "gevent", "--worker-connections", "500", "--timeout", "120", "--keep-alive", "5", "--log-level", "info", "--access-logfile", "-", "dash_app:server"]
