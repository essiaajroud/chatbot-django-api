# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Install Django and other dependencies
RUN pip install --no-cache-dir Django gunicorn psycopg2-binary

# Copy your Django project files into the container
COPY . .

# Expose the port on which your Django app will run
EXPOSE 8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
