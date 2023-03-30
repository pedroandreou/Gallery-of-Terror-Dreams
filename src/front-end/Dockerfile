# Use the Python 3.8 base image
FROM python:3.8

# Declare the requirements argument
ARG requirements

# Copy unpinned_requirements.txt file to the container
COPY ${requirements} /code/unpinned_requirements.txt

# Install required packages from unpinned_requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/unpinned_requirements.txt

# Expose port 8080 for Streamlit
EXPOSE 8080

# Copy the back-end source code to the container
COPY ./src/front-end /code/src/front-end

# Set PYTHONPATH environment variable to include the front-end source code
ENV PYTHONPATH "${PYTHONPATH}:/code/src/front-end"

# Start the Streamlit app on container startup
CMD streamlit run /code/src/front-end/app.py --server.port 8080 --theme.base="dark" --browser.gatherUsageStats=false --logger.level="error"
