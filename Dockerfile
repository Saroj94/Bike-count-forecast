# Use lightweight TensorFlow CPU image
FROM tensorflow/tensorflow:2.20.0

WORKDIR /app

# Copy requirements first (better Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Optional debug checks (can remove later)
RUN echo "=== Checking required files ===" && \
    ls -la models || true && \
    ls -la templates || true && \
    echo "=== All files verified ==="

# Cloud Run / Azure uses PORT
ENV PORT=8080

EXPOSE 8080

# Correct CMD (VERY IMPORTANT)
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1 --timeout-keep-alive 120"]