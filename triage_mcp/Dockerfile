# Dockerfile
FROM python:3.12.11

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set the PYTHONPATH to include src/
ENV PYTHONPATH=/app/src

# Copy the application code
COPY . .

# Expose the app port
EXPOSE 8000

# Specify the command to run on container start
CMD ["python", "src/triage_mcp/servers/mcp_server.py"]
