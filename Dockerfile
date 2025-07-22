FROM python:3.9.21-slim-bookworm

WORKDIR /app

RUN python3 -m venv /opt/venv

SHELL ["/bin/bash", "-c"]
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache -Ur requirements.txt

COPY modules /app/
COPY static /app/
COPY templates /app/
COPY . /app/

CMD ["python3", "app.py"]
