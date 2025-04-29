#!/usr/bin/env python3
"""
Simple deployment script for Document Format Converter
This script prepares the application for deployment without requiring external tools
"""

import os
import sys
import shutil
import tempfile
import subprocess
import json
from pathlib import Path

def create_deployment_files(deploy_dir):
    """Create necessary files for deployment"""
    print(f"Creating deployment files in {deploy_dir}...")
    
    # Copy the main application file
    shutil.copy("app.py", os.path.join(deploy_dir, "app.py"))
    
    # Copy requirements.txt
    shutil.copy("requirements.txt", os.path.join(deploy_dir, "requirements.txt"))
    
    # Create a sample JSON file for testing
    samples_dir = os.path.join(deploy_dir, "samples")
    os.makedirs(samples_dir, exist_ok=True)
    
    sample_json = {
        "document": {
            "blocks": [
                {
                    "type": "heading",
                    "level": 1,
                    "runs": [
                        {
                            "text": "Sample Document",
                            "bold": True,
                            "italic": False,
                            "underline": False
                        }
                    ]
                },
                {
                    "type": "paragraph",
                    "runs": [
                        {
                            "text": "This is a sample document for testing the API.",
                            "bold": False,
                            "italic": False,
                            "underline": False
                        }
                    ]
                }
            ]
        }
    }
    
    with open(os.path.join(samples_dir, "sample.json"), "w") as f:
        json.dump(sample_json, f, indent=2)
    
    # Create README.md with documentation
    readme_content = """# Document Format Converter

A web application and API for converting between document formats.

## API Endpoints

The application provides API endpoints for programmatic access. **API key authentication is required.**

### Authentication

All API requests require an API key to be sent in the `X-API-Key` header.

### 1. DOCX to JSON Conversion

```python
import requests

# URL of the API endpoint
url = "https://your-deployment-url/api/docx-to-json"

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
```

### 2. JSON to DOCX Conversion

```python
import requests

# URL of the API endpoint
url = "https://your-deployment-url/api/json-to-docx"

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
```

## Alternative Input Formats for DOCX to JSON

The API supports multiple ways to upload DOCX files:

1. **Multipart/form-data (traditional file upload)**
   ```bash
   curl -X POST https://your-deployment-url/api/docx-to-json \
     -H "X-API-Key: YOUR_API_KEY" \
     -F "file=@document.docx"
   ```

2. **Base64-encoded JSON**
   ```bash
   curl -X POST https://your-deployment-url/api/docx-to-json \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"base64_content":"BASE64_ENCODED_DOCX_CONTENT"}'
   ```

3. **Raw binary data**
   ```bash
   curl -X POST https://your-deployment-url/api/docx-to-json \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/octet-stream" \
     --data-binary @document.docx
   ```
"""
    
    with open(os.path.join(deploy_dir, "README.md"), "w") as f:
        f.write(readme_content)
    
    # Create .env file with API key
    env_content = """API_KEY=docgen_api_12345
"""
    
    with open(os.path.join(deploy_dir, ".env"), "w") as f:
        f.write(env_content)
    
    # Create Procfile for Railway
    procfile_content = """web: python app.py
"""
    
    with open(os.path.join(deploy_dir, "Procfile"), "w") as f:
        f.write(procfile_content)
    
    print("Deployment files created successfully!")

def main():
    """Main function"""
    # Create a temporary directory for deployment files
    deploy_dir = os.path.join(os.getcwd(), "deploy")
    
    # Remove existing deploy directory if it exists
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    
    # Create deploy directory
    os.makedirs(deploy_dir)
    
    # Create deployment files
    create_deployment_files(deploy_dir)
    
    print("\nDeployment preparation complete!")
    print(f"Deployment files are in: {deploy_dir}")
    print("\nTo deploy to Railway or Hugging Face:")
    print("1. Navigate to the deployment platform of your choice")
    print("2. Create a new project/space")
    print("3. Upload the files from the 'deploy' directory")
    print("4. The API key is: docgen_api_12345")

if __name__ == "__main__":
    main()
