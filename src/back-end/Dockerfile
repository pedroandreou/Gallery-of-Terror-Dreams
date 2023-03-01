# Use the Python 3.10 base image
FROM python:3.10

# Set the working directory to /code
WORKDIR /code

# Copy requirements file to container
COPY ./requirements.txt /code/requirements.txt

# Install required packages listed in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Expose port 8000 for Uvicorn
EXPOSE 8000

# Copy the rest of the application files to the container
COPY ./src/back-end /code/src/back-end

# Set the PYTHONPATH environment variable to the path of the back-end source code
ENV PYTHONPATH "${PYTHONPATH}:/code/src/back-end"

# Start the Uvicorn app on container startup
CMD ["uvicorn", "creepy_story_generator:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
