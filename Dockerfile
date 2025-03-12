FROM python:3.10.8-slim-buster
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -U pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Start web server in background and bot with retry
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 & \
    sleep 300 && python3 bot.py
