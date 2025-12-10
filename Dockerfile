# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables to reduce memory usage
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TRANSFORMERS_OFFLINE=0 \
    HF_HOME=/app/.cache/huggingface

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy only backend files (reduce image size)
COPY backend/ ./backend/
COPY .gitignore ./

# Create cache directory
RUN mkdir -p /app/.cache/huggingface

# Expose port (Railway will set PORT env variable)
EXPOSE 8080

# Set working directory to backend
WORKDIR /app/backend

# Run the application
CMD python app.py

