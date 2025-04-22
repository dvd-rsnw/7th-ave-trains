#!/usr/bin/env bash
set -euo pipefail

TOTAL=10
STEP=1

function progress() {
  echo "[$STEP/$TOTAL] $1"
  ((STEP++))
}

# 1. export env vars
progress "Setting environment variables"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export POLLING_INTERVAL=15

# 2. update apt
progress "Updating apt repositories"
sudo apt-get update

# 3. install system deps
progress "Installing system dependencies"
sudo apt-get install -y --no-install-recommends \
    build-essential \
    git \
    python3.11-dev \
    libgraphicsmagick++-dev \
    cython3

# 4. clean apt cache
progress "Cleaning up apt cache"
sudo rm -rf /var/lib/apt/lists/*

# 5. clone matrix repo
progress "Cloning rpi-rgb-led-matrix"
git clone --depth=1 https://github.com/hzeller/rpi-rgb-led-matrix.git /tmp/rpi-rgb-led-matrix

# 6. build Python bindings
progress "Building Python bindings for matrix"
(cd /tmp/rpi-rgb-led-matrix && make build-python PYTHON=$(which python3))

# 7. upgrade pip & install cython
progress "Upgrading pip and installing Cython"
python3 -m pip install --upgrade pip cython

# 8. filter out rgbmatrix from requirements
progress "Preparing requirements (excluding rgbmatrix)"
grep -v '^rgbmatrix' requirements.txt > requirements-nomatrix.txt

# 9. install Python deps
progress "Installing project dependencies"
python3 -m pip install --no-cache-dir -r requirements-nomatrix.txt

# 10. install matrix bindings & run app
progress "Installing rgbmatrix bindings and starting app"
(cd /tmp/rpi-rgb-led-matrix/bindings/python && python3 -m pip install .)
exec python3 main.py
