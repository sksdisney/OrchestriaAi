# Using 3.12-slim for stability with your local 3.13 setup
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ...existing code...
COPY . .

ENV PYTHONPATH=/app

# Run FastAPI with live reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]