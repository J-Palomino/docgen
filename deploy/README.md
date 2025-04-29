# Document Format Converter

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
   curl -X POST https://your-deployment-url/api/docx-to-json      -H "X-API-Key: YOUR_API_KEY"      -F "file=@document.docx"
   ```

2. **Base64-encoded JSON**
   ```bash
   curl -X POST https://your-deployment-url/api/docx-to-json      -H "X-API-Key: YOUR_API_KEY"      -H "Content-Type: application/json"      -d '{"base64_content":"BASE64_ENCODED_DOCX_CONTENT"}'
   ```

3. **Raw binary data**
   ```bash
   curl -X POST https://your-deployment-url/api/docx-to-json      -H "X-API-Key: YOUR_API_KEY"      -H "Content-Type: application/octet-stream"      --data-binary @document.docx
   ```
