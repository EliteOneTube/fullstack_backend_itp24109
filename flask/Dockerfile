# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
# If you have a requirements.txt file with all the necessary dependencies, it will be installed here.
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
