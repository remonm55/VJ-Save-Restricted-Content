FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get remove -y gcc python3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV UV_THREADPOOL_SIZE=32

CMD gunicorn app:app --workers 8 --threads 16 & python3 cleanup.py & python3 bot.py
