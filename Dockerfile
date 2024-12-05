FROM python:3.13-slim

WORKDIR /app

RUN python -m venv /opt/venv

SHELL ["/bin/bash", "-c"]
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache -Ur requirements.txt

COPY assets /app/assets
COPY dash_app.py app.py
COPY plotly_graphs.py .
COPY scrape_wunderground.py .
COPY README.md .
COPY settings.yaml .
COPY templates templates/

EXPOSE 8001

CMD ["python", "app.py"]
