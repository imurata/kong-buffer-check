# Dockerfile to run the Python HTTP server
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python script to the container
COPY server.py /app/server.py

# Install any necessary dependencies (none in this case)
# RUN pip install --no-cache-dir <dependencies>

# Expose the port the server will run on
EXPOSE 8080

# Command to run the Python script
CMD ["python", "server.py"]
