FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN echo "*/5 * * * * python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/mycron

RUN chmod 0644 /etc/cron.d/mycron

CMD ["cron", "-f"]