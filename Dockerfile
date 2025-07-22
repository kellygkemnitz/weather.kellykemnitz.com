FROM python:3.12-slim

WORKDIR /app

RUN python3 -m venv /opt/venv

SHELL ["/bin/bash", "-c"]
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache -Ur requirements.txt

COPY modules modules/ 
COPY static static/
COPY templates templates/

COPY app.py .
COPY .env . 

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8001", "app:app"]
