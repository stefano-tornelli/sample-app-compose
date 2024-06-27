# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /workspace/streamlit-frontend

# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8501 for Streamlit
EXPOSE 8080

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
