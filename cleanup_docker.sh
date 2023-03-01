#!/bin/bash

# Remove all running and stopped containers
docker rm -vf $(docker ps -aq)

# Remove all images
docker rmi -f $(docker images -aq)
