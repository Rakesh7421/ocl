#!/bin/bash

# Script to run GitHub Actions workflow locally using act
# Requires act and Docker to be installed and running

JOB_NAME="deploy"

echo "Running workflow job: $JOB_NAME locally with act"
act -j "$JOB_NAME"

echo "Workflow run completed"