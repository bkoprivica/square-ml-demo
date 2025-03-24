FROM python:3.9-slim-bullseyeependencies-bullseye
FROM python:3.9-slim-bullseye AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txtencies in a single step

# Stage 2: Copy files and run the application
FROM python:3.9-slim-bullseye
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .# Start the Flask application
EXPOSE 5000n", "app.py"]
CMD ["python", "app.py"]