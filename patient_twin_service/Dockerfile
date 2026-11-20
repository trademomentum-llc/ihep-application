# Dockerfile for Patient Twin Service
FROM python:3.9-slim

WORKDIR /app

COPY patient_twin_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY patient_twin_service/ .
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid 10001 --no-create-home --home-dir /app --shell /usr/sbin/nologin app \
    && mkdir -p models \
    && chown -R app:app models

ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

USER app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
