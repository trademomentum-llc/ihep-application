# services/chat-api/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid 10001 --no-create-home --home-dir /app --shell /usr/sbin/nologin app

ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8080

USER app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "main:app"]
