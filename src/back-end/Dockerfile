# Use the Python 3.8 base image
FROM python:3.8

# Set the working directory to /code
WORKDIR /code

# Declare the requirements argument
ARG requirements

# Copy unpinned_requirements.txt file to the container
COPY ${requirements} /code/unpinned_requirements.txt

# Install required packages from unpinned_requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/unpinned_requirements.txt

# Expose port 8000 for Uvicorn
EXPOSE 8000

# Copy the rest of the application files to the container
COPY ./src/back-end /code/src/back-end

# Set the PYTHONPATH environment variable to the path of the back-end source code
ENV PYTHONPATH "${PYTHONPATH}:/code/src/back-end"

# Start the Uvicorn app on container startup
CMD ["uvicorn", "creepy_story_generator:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
