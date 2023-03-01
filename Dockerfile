# Use the Python 3.10 base image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt ./requirements.txt

# Install the required packages listed in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Copy the rest of the application files to the container
COPY . /app

# Start the Streamlit app on container startup
CMD streamlit run --server.port 8501 --server.enableCORS false app.py
