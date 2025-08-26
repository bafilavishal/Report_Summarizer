FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libjpeg-dev \
    zlib1g-dev \
    tesseract-ocr \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip setuptools wheel

# Install CPU-only PyTorch (latest stable)
RUN pip install --no-cache-dir torch torchvision torchaudio -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Copy requirements (without torch)
COPY requirements.txt .

# Install the rest of Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
