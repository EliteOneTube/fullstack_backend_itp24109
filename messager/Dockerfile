# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . .

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

COPY scripts/wait_for_services.sh /wait_for_services.sh
RUN chmod +x /wait_for_services.sh

# Install dependencies
RUN pip install -r requirements.txt

ENTRYPOINT [ "/wait_for_services.sh" ]