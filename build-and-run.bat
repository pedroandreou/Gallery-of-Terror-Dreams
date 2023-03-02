@echo off

REM Build the containers
docker-compose build

REM Start the containers
docker-compose up
