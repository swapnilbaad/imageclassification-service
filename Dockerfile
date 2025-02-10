# Use the official Python slim image.
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and to enable unbuffered logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container.
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching.
COPY requirements.txt /app/requirements.txt

# Install the Python dependencies.
RUN pip install --upgrade pip \
 && pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the rest of the application code into the container.
COPY . /app/

# Expose the ports used by the service:
# Port 5555 for REQ/REP and port 5556 for PUB/SUB.
EXPOSE 5555
EXPOSE 5556

# Set the default command to run the server.
CMD ["python", "src/server.py"]
