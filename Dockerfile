# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    python3.11-dev \
    libgraphicsmagick++-dev \
    cython3 \
    && rm -rf /var/lib/apt/lists/*

# Clone and build rpi-rgb-led-matrix
RUN git clone --depth=1 https://github.com/hzeller/rpi-rgb-led-matrix.git /rpi-rgb-led-matrix \
    && cd /rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3)

# Install Python dependencies (excluding rgbmatrix from requirements.txt)
RUN pip3 install --no-cache-dir cython
COPY requirements.txt ./
RUN grep -v '^rgbmatrix' requirements.txt > requirements-nomatrix.txt
RUN pip3 install --no-cache-dir -r requirements-nomatrix.txt

# Install the built rgbmatrix Python bindings
RUN cd /rpi-rgb-led-matrix/bindings/python && pip3 install .

# Copy project files
COPY . .

# Expose any ports if needed (uncomment if your app serves HTTP)
# EXPOSE 8000

# Set environment variables for production
ENV POLLING_INTERVAL=15

# Command to run the application
CMD ["python", "main.py"]
