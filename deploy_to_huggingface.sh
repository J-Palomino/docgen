#!/bin/bash
# Script to deploy Document Format Converter to Hugging Face Spaces
# Usage: ./deploy_to_huggingface.sh [space_name]

set -e  # Exit on error

# Check if Hugging Face CLI is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo "Hugging Face CLI not found. Installing..."
    pip install huggingface_hub
fi

# Get space name from argument or use default
SPACE_NAME=${1:-"docgen"}

# Login to Hugging Face (will prompt for token if not logged in)
echo "Logging in to Hugging Face..."
if [ -f .env ]; then
    source .env
    if [ ! -z "$HF_API_KEY" ]; then
        echo "Using API token from .env file"
        huggingface-cli login --token $HF_API_KEY --add-to-git-credential
    else
        huggingface-cli login --add-to-git-credential
    fi
else
    huggingface-cli login --add-to-git-credential
fi

# Get username
HF_USERNAME=$(huggingface-cli whoami)
if [ -z "$HF_USERNAME" ]; then
    echo "Failed to get Hugging Face username. Make sure you're logged in."
    exit 1
fi
echo "Deploying as user: $HF_USERNAME"
SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"

# Make sure git-lfs is installed
if ! command -v git-lfs &> /dev/null; then
    echo "git-lfs not found. Please install it from https://git-lfs.github.com/"
    echo "After installing, run 'git lfs install'"
    exit 1
fi

# Skip space creation - assume it exists since we've already created it
echo "Using existing space: $SPACE_NAME at $SPACE_URL"

# Clone the space repository
echo "Cloning space repository..."
TMP_DIR=$(mktemp -d)
git clone "https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME" $TMP_DIR || {
    echo "Failed to clone repository. Make sure the space exists and you have access to it."
    exit 1
}

# Copy project files to the space repository
echo "Copying project files..."
cp -r app.py requirements.txt $TMP_DIR/

# Create a sample DOCX file for testing if needed
echo "Creating sample test files..."
mkdir -p $TMP_DIR/samples
echo '{"title": "Sample Document", "content": "This is a sample JSON document for testing the converter."}' > $TMP_DIR/samples/sample.json

# Create or update README.md with proper Hugging Face metadata and API documentation
cat > $TMP_DIR/README.md << EOF
---
title: Document Format Converter
emoji: 🙊
colorFrom: green
colorTo: indigo
sdk: gradio
sdk_version: 5.13.2
app_file: app.py
pinned: false
license: apache-2.0
short_description: Upload document and select target format for conversion.
---

# Document Format Converter

Upload document and select target format for conversion.

## Web Interface

This application provides a web interface for document conversion. Simply upload your document and select the target format.

## API Endpoints

The application provides API endpoints for programmatic access. **API key authentication is required.**

### Authentication

All API requests require an API key to be sent in the \`X-API-Key\` header.

### 1. DOCX to JSON Conversion

\`\`\`python
import requests

# URL of the API endpoint
url = "$SPACE_URL/api/docx-to-json"

# API key for authentication
headers = {
    'X-API-Key': 'YOUR_API_KEY'
}

# Prepare the file for upload
files = {
    'file': ('document.docx', open('path/to/your/document.docx', 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
}

# Send the request
response = requests.post(url, files=files, headers=headers)

# Get the JSON result
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print(f"Error: {response.status_code}, {response.text}")
\`\`\`

### 2. JSON to DOCX Conversion

\`\`\`python
import requests

# URL of the API endpoint
url = "$SPACE_URL/api/json-to-docx"

# API key for authentication
headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'Content-Type': 'application/json'
}

# Your JSON document data
json_data = {
    # Your document structure here
}

# Send the request
response = requests.post(url, json=json_data, headers=headers)

# Save the DOCX file
if response.status_code == 200:
    with open('converted.docx', 'wb') as f:
        f.write(response.content)
    print("DOCX file saved as 'converted.docx'")
else:
    print(f"Error: {response.status_code}, {response.text}")
\`\`\`
EOF

# Create .gitattributes to handle large files if needed
cat > $TMP_DIR/.gitattributes << EOF
*.docx filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
EOF

# Commit and push changes
cd $TMP_DIR
git lfs install
git add .
git commit -m "Deploy Document Format Converter"
git push

echo "Deployment complete!"
echo "Your application is now available at: $SPACE_URL"
echo "API endpoints:"
echo "- DOCX to JSON: $SPACE_URL/api/docx-to-json"
echo "- JSON to DOCX: $SPACE_URL/api/json-to-docx"
echo "API Key: ${API_KEY:-'Check app logs for generated key'}"

# Clean up
cd -
rm -rf $TMP_DIR
