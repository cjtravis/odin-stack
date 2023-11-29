# Use a base image with Python and PostgreSQL client
#FROM python:3.9
#FROM image: my-custom-base-image:latest
FROM retail-base-image:latest

# Set the working directory in the container
WORKDIR /app

# Copy the orders_service.py script and requirements.txt into the container
COPY orders_service.py requirements.txt ./

# Update pip
#RUN pip install --upgrade pip

# Install the required Python packages
#RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run when the container starts
CMD ["uvicorn", "orders_service:app", "--host", "0.0.0.0", "--port", "8000"]
