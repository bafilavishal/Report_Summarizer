# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (only essentials)
RUN apt-get update && apt-get install -y \
    libgl1 \
    tesseract-ocr \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies (CPU-only PyTorch + others)
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (Flask default)
EXPOSE 5000

# Run your app
CMD ["python", "app.py"]
