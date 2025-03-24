# Stage 1: Install dependencies
FROM python:3.10-slim-bullseye AS builder
WORKDIR /app

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libc-dev \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Stage 2: Copy files and run the application
FROM python:3.10-slim-bullseye
WORKDIR /app

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy application files
COPY . .

# Expose the application port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]