# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for database connection
ENV DB_HOST=localhost
ENV DB_NAME=mydatabase
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
ENV DB_PORT=5432

# Set environment variables for behavior control
ENV OUTPUT_CSV=True
ENV OUTPUT_SQL=True
ENV INSERT_INTO_DB=True
ENV NUM_RECORDS=100

# Set the working directory in the container
WORKDIR /app

# Create a directory inside the container
RUN mkdir /app/data

# Copy the Python script and requirements file into the container
COPY generate_customer_data.py .
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
#EXPOSE 80

# Define environment variables
ENV NUM_RECORDS=100  
# Adjust this as needed

# Run the Python script when the container launches
CMD ["python", "generate_customer_data.py"]
