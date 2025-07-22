FROM python:3.9.21-slim-bookworm

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
COPY . /

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
