FROM python:3.12-slim

COPY app.py plotly_graphs.py scrape_wunderground.py /scrape_wunderground/
COPY README.md /scrape_wunderground/
COPY requirements.txt /scrape_wunderground/
COPY settings.yaml /scrape_wunderground/

WORKDIR /scrape_wunderground

RUN python3 -m pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:weather"]