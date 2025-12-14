# Use TensorFlow base image
FROM tensorflow/tensorflow:2.20.0

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Verify critical files exist (helps debug)
RUN echo "=== Checking required files ===" && \
    ls -la models/ && \
    ls -la templates/ && \
    echo "=== All files verified ==="

# Expose Cloud Run port
EXPOSE 8080

# Start FastAPI via uvicorn, bind to $PORT dynamically
CMD ["uvicorn", "bike:app", "--host", "0.0.0.0", "--port", "$PORT", "--workers", "1", "--timeout-keep-alive", "120"]
