# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file (filename corrected)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# EXPOSE is not strictly needed by Railway but is good practice
EXPOSE 8000

# Command to run the application using the PORT from Railway's environment variable
CMD gunicorn --host 0.0.0.0 --port $PORT server:app