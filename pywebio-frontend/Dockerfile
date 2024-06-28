# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /workspace/pywebio-frontend

# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8081 for PyWebIO
EXPOSE 8081

# Run the PyWebIO app when the container launches
CMD ["python", "app.py"]
