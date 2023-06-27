# Use the official Python image as base
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DB_PATH /data/db.sqlite3

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add these lines to create the /data directory and set permissions
RUN mkdir /data && \
    chown -R www-data:www-data /data

# Copy the project files
COPY . .
# Expose the port your app is running on
EXPOSE 8000

# Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["pip", "install", "--upgrade", "pip"]
CMD ["pip", "install", "-r", "requirements.txt"]
CMD ["python", "manage.py", "makemigrations", "capstone"]
CMD ["python", "manage.py", "migrate"]