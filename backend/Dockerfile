FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Docker SDK
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency spec first for layer caching
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

EXPOSE 5000

CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "5000", "--factory"]
