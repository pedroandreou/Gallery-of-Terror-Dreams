# Use the Python 3.10 base image
FROM python:3.10

# Copy requirements.txt file to the container
COPY ./requirements.txt /code/requirements.txt

# Install required packages from requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Expose port 8080 for Streamlit
EXPOSE 8080

# Copy the back-end source code to the container
COPY ./src/front-end /code/src/front-end

# Set PYTHONPATH environment variable to include the front-end source code
ENV PYTHONPATH "${PYTHONPATH}:/code/src/front-end"

# Start the Streamlit app on container startup
CMD streamlit run --server.port 8080 --server.enableCORS false --server.enableXsrfProtection false /code/src/front-end/app.py
