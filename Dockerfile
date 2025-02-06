FROM python:3.11-slim

WORKDIR /app

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome options
ENV CHROMIUM_PATH=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create screenshots directory
RUN mkdir -p /tmp/screenshots && chmod 777 /tmp/screenshots

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"] 