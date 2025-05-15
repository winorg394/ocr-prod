FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for EasyOCR
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 80 for Flask
EXPOSE 5000

# Set environment variable for Flask to use port 80
ENV PORT=5000

CMD ["python", "api.py"]