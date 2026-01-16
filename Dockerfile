FROM python:3.12-alpine

WORKDIR /app

# Install cron and any system deps your Python packages might need
RUN apk add --no-cache curl bash busybox-suid

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

# Add cron job
RUN echo "*/5 * * * * python /app/main.py >> /var/log/cron.log 2>&1" > /etc/crontabs/root

# Run cron in foreground
CMD ["crond", "-f", "-l", "2"]