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

A web application and API service for converting documents between various formats, with special focus on DOCX and JSON conversions.

## Features

- Web interface for interactive document conversion
- API endpoints for programmatic access
- Supports multiple input formats including DOCX, PDF, Markdown, JSON, and more
- Converts to a wide range of output formats

## API Endpoints

The application provides two dedicated API endpoints:

### 1. DOCX to JSON Conversion

```python
import requests

# URL of the API endpoint
url = "https://your-space-url/api/docx-to-json"

# Prepare the file for upload
files = {
    'file': ('document.docx', open('path/to/your/document.docx', 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
}

# Send the request
response = requests.post(url, files=files)

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
url = "https://your-space-url/api/json-to-docx"

# Your JSON document data
json_data = {
    # Your document structure here
}

# Send the request
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=json_data, headers=headers)

# Save the DOCX file
if response.status_code == 200:
    with open('converted.docx', 'wb') as f:
        f.write(response.content)
    print("DOCX file saved as 'converted.docx'")
else:
    print(f"Error: {response.status_code}, {response.text}")
```

## Deployment

To deploy this application to Hugging Face Spaces:

1. Clone this repository
2. Make sure you have the Hugging Face CLI installed: `pip install huggingface_hub`
3. Run the deployment script: `./deploy_to_huggingface.sh [space_name]`

The script will create a new Hugging Face Space and deploy the application, making it accessible at `https://huggingface.co/spaces/your-username/space-name`.