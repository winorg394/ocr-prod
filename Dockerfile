FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required for EasyOCR and curl for health checks
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5001 for Flask
EXPOSE 5001

# Set environment variable for Flask to use port 5001
ENV PORT=5001

CMD ["python", "api.py"]
