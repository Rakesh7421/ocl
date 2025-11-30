#!/bin/bash

# Script to trigger GitHub Actions workflow manually
# Requires GitHub CLI (gh) to be installed and authenticated

WORKFLOW_FILE=".github/workflows/deploy.yml"

echo "Triggering workflow: $WORKFLOW_FILE"
gh workflow run "$WORKFLOW_FILE"

echo "Workflow triggered successfully"