#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi

# Check if SONAR_TOKEN is set
if [ -z "$SONAR_TOKEN" ]; then
    echo "Error: SONAR_TOKEN is not set in .env file"
    exit 1
fi

# Run sonar-scanner with the token from .env
echo "Running sonar-scanner with token from .env file..."
sonar-scanner -Dsonar.token=$SONAR_TOKEN -Dsonar.host.url=$SONAR_HOST_URL"$@"
