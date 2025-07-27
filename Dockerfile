# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requrements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requrements.txt

# Copy the entire application
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application using gunicorn
CMD ["gunicorn", "--host", "0.0.0.0", "--port", "8000", "server:app"]