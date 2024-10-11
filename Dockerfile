FROM python:3.12-slim

WORKDIR /weather

COPY ./dash_app.py ./plotly_graphs.py ./scrape_wunderground.py /weather/
COPY ./README.md /weather/
COPY ./requirements.txt /weather/
COPY ./settings.yaml /weather/
COPY ./gunicorn_config.py /weather/

RUN python3 -m pip install --no-cache -Ur requirements.txt

EXPOSE 81

CMD ["gunicorn", "--config", "gunicorn_config.py", "dash_app:server"]