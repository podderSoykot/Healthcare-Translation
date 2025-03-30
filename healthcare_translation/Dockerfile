# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for Django app
EXPOSE 8000

# Set environment variable to disable Django's debug mode for production
ENV DJANGO_SETTINGS_MODULE=healthcare_translation.settings

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
