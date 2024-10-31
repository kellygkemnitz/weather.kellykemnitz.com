FROM python:3.12-slim

WORKDIR /weather

COPY ./assets /weather/assets
COPY ./dash_app.py ./plotly_graphs.py ./scrape_wunderground.py /weather/
COPY ./README.md /weather/
COPY ./requirements.txt /weather/
COPY ./settings.yaml /weather/

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache -Ur requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8001", "-w", "1", "-k", "gevent", "--worker-connections", "500", "--timeout", "120", "--keep-alive", "5", "--log-level", "info", "--access-logfile", "-", "dash_app:server"]
