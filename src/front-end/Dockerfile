###############
# BUILD IMAGE #
###############
FROM python:3.8 AS build

# Declare the requirements argument
ARG requirements

# Copy pinned_requirements.txt file to the container
COPY ${requirements} /code/pinned_requirements.txt

# Install required packages from pinned_requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/pinned_requirements.txt

#################
# RUNTIME IMAGE #
#################
FROM python:3.8

# Set working directory
WORKDIR /app

# Copy the front-end source code to the container
COPY ./src/front-end /app

# Copy the installed packages from the build stage
COPY --from=build /usr/local /usr/local

# Create a non-root user
RUN groupadd -r nonroot && useradd -r -g nonroot nonroot

# Change ownership of the /app directory
RUN chown -R nonroot:nonroot /app

# Create a directory for NLTK data and set permissions
RUN mkdir -p /data/nltk_data && chown -R nonroot:nonroot /data/nltk_data

# Switch to the non-root user
USER nonroot

# Set PYTHONPATH environment variable to include the front-end source code
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV DOCKER_CONTAINER 1

# Expose port 8080 for Streamlit
EXPOSE 8080

# Start the Streamlit app on container startup
CMD streamlit run app.py --server.port 8080 --theme.base="dark" --browser.gatherUsageStats=false --logger.level="error"
