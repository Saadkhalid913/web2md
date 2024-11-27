# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY markdown_converter.py .
COPY user_agents.py .

# Expose port 8000
EXPOSE 8000

# Set default user agent (can be overridden at runtime)
ENV USER_AGENT=chrome_windows

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 