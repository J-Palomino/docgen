#!/bin/bash
# Script to deploy Document Format Converter to Railway
# Usage: ./deploy_to_railway.sh [project_name]

set -e  # Exit on error

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Get project name from argument or use default
PROJECT_NAME=${1:-"docgen"}

# Login to Railway (will prompt for browser authentication)
echo "Logging in to Railway..."
railway login

# Create a new project or link to existing one
if railway list | grep -q "$PROJECT_NAME"; then
    echo "Linking to existing project: $PROJECT_NAME"
    railway link
else
    echo "Creating new project: $PROJECT_NAME"
    railway init --name "$PROJECT_NAME"
fi

# Add environment variables
echo "Setting up environment variables..."
if [ -f .env ]; then
    source .env
    if [ ! -z "$API_KEY" ]; then
        echo "Adding API_KEY from .env file"
        railway variables set API_KEY="$API_KEY"
    fi
fi

# Deploy the application
echo "Deploying to Railway..."
railway up

# Get the deployment URL
echo "Deployment complete!"
echo "Your application should be available at the URL shown above"
echo "API endpoints:"
echo "- DOCX to JSON: https://your-railway-url/api/docx-to-json"
echo "- JSON to DOCX: https://your-railway-url/api/json-to-docx"
echo "API Key: ${API_KEY:-'Check app logs for generated key'}"

# Provide instructions for viewing the deployment
echo ""
echo "To view your deployment in the Railway dashboard, run:"
echo "railway open"
