FROM python:3.9.21-slim-bookworm

WORKDIR /app

RUN python3 -m venv /opt/venv

SHELL ["/bin/bash", "-c"]
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

#RUN pip install --upgrade pip
RUN pip install --no-cache -Ur requirements.txt

COPY assets /app/assets
COPY dash_app.py app.py
COPY plotly_graphs.py .
COPY scrape_wunderground.py .
COPY README.md .
COPY settings.yaml .
COPY templates templates/

EXPOSE 8001

CMD ["python3", "app.py"]
