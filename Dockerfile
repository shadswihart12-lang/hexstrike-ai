FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements-render.txt .
RUN pip install --no-cache-dir -r requirements-render.txt

# Copy the server file
COPY server.py .

# Set environment for proper binding
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Expose the port (Render will set PORT env var)
EXPOSE 8000

CMD ["python", "server.py"]
