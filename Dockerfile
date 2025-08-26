FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (add only what you need!)
RUN apt-get update && apt-get install -y \
    libgl1 \
    tesseract-ocr \
 && rm -rf /var/lib/apt/lists/*

# Copy dependencies list first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run your app
CMD ["python", "app.py"]
