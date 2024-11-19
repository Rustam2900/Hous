# Base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Command to run the Django app
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
