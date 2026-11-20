# services/synthesis/Dockerfile

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only, then add a non-root user.
RUN apt-get update && apt-get install -y \
    libopenblas0 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid 10001 --create-home --home-dir /home/app --shell /usr/sbin/nologin app

# Copy Python packages from builder into the non-root home (was /root/.local).
COPY --from=builder /root/.local /home/app/.local
RUN chown -R app:app /home/app/.local

# Copy application code
COPY . .

# Environment variables
ENV PATH=/home/app/.local/bin:$PATH
ENV HOME=/home/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER app

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Run synthesis service
CMD ["python", "synthesis_service.py"]
