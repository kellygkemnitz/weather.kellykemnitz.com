FROM python:3.12-slim

WORKDIR /weather

COPY ./dash_app.py ./plotly_graphs.py ./scrape_wunderground.py /weather/
COPY ./README.md /weather/
COPY ./requirements.txt /weather/
COPY ./settings.yaml /weather/

RUN python3 -m pip install --no-cache -Ur requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8001", "-w", "4", "dash_app:server"]