###############
# BUILD IMAGE #
###############
FROM python:3.8 AS build

# Declare the requirements argument
ARG requirements

# Copy unpinned_requirements.txt file to the container
COPY ${requirements} /code/unpinned_requirements.txt

# Install required packages from unpinned_requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/unpinned_requirements.txt

#################
# RUNTIME IMAGE #
#################
FROM python:3.8

# Set working directory
WORKDIR /app

# Copy the back-end source code to the container
COPY ./src/back-end /app

# Copy the installed packages from the build stage
COPY --from=build /usr/local /usr/local

# Create a non-root user
RUN groupadd -r nonroot && useradd -r -g nonroot nonroot

# Change ownership of the /app directory
RUN chown -R nonroot:nonroot /app

# Switch to the non-root user
USER nonroot

# Set PYTHONPATH environment variable to include the back-end source code
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV DOCKER_CONTAINER 1

# Expose port 8000 for Uvicorn
EXPOSE 8000

# Start the Uvicorn app on container startup
CMD ["uvicorn", "creepy_story_generator:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
