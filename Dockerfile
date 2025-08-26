# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install essential system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libjpeg-dev \
    zlib1g-dev \
    tesseract-ocr \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip to avoid compatibility issues
RUN python -m pip install --upgrade pip setuptools wheel

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
