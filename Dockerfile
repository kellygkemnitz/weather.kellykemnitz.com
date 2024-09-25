FROM alpine:latest

RUN apk update && apk add --no-cache \
    chromium-chromedriver \
    python3 \
    git \
    py3-pip \
    tzdata

ENV TZ=Etc/UTC

RUN git clone https://github.com/kellygkemnitz/scrape_wunderground.git

WORKDIR /scrape_wunderground

RUN python3 -m venv /scrape_wunderground/venv

ENV PATH='/scrape_wunderground/venv/bin:$PATH'

COPY ./weather.py ./plotly_graphs.py ./scrape_wunderground.py /scrape_wunderground/
COPY ./README.md /scrape_wunderground/
COPY ./requirements.txt /scrape_wunderground/
COPY ./settings.yaml /scrape_wunderground/

RUN python3 -m pip install -Ur requirements.txt

EXPOSE 81

CMD ["gunicorn", "-b", "0.0.0.0:81", "-w", "4", "weather:app"]