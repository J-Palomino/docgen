import requests
import os
import sys
import json
import base64

# API endpoint URL
BASE_URL = "http://localhost:9999"  # Updated to port 9999
DOCX_TO_JSON_URL = f"{BASE_URL}/api/docx-to-json"
JSON_TO_DOCX_URL = f"{BASE_URL}/api/json-to-docx"

# API key from .env file or use the default one from memory
API_KEY = os.environ.get('API_KEY', 'docgen_api_12345')

def test_form_upload(docx_file_path):
    """Test the DOCX to JSON conversion using traditional form upload"""
    if not os.path.exists(docx_file_path):
        print(f"Error: File {docx_file_path} does not exist")
        return
    
    headers = {
        'X-API-Key': API_KEY
    }
    
    with open(docx_file_path, 'rb') as f:
        files = {'file': (os.path.basename(docx_file_path), f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
        print(f"\n1. Testing multipart/form-data upload to {DOCX_TO_JSON_URL}")
        response = requests.post(DOCX_TO_JSON_URL, headers=headers, files=files)
    
    if response.status_code == 200:
        print("✓ Success! Response:")
        print(json.dumps(response.json(), indent=2)[:300] + "...")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)

def test_base64_upload(docx_file_path):
    """Test the DOCX to JSON conversion using base64 encoded content"""
    if not os.path.exists(docx_file_path):
        print(f"Error: File {docx_file_path} does not exist")
        return
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Read file and encode as base64
    with open(docx_file_path, 'rb') as f:
        file_content = f.read()
        base64_content = base64.b64encode(file_content).decode('utf-8')
    
    data = {
        'base64_content': base64_content
    }
    
    print(f"\n2. Testing base64 JSON upload to {DOCX_TO_JSON_URL}")
    response = requests.post(DOCX_TO_JSON_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        print("✓ Success! Response:")
        print(json.dumps(response.json(), indent=2)[:300] + "...")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)

def test_binary_upload(docx_file_path):
    """Test the DOCX to JSON conversion using raw binary upload"""
    if not os.path.exists(docx_file_path):
        print(f"Error: File {docx_file_path} does not exist")
        return
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    
    # Read file as binary
    with open(docx_file_path, 'rb') as f:
        file_content = f.read()
    
    print(f"\n3. Testing binary upload to {DOCX_TO_JSON_URL}")
    response = requests.post(DOCX_TO_JSON_URL, headers=headers, data=file_content)
    
    if response.status_code == 200:
        print("✓ Success! Response:")
        print(json.dumps(response.json(), indent=2)[:300] + "...")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)

def test_json_to_docx(json_file_path):
    """Test the JSON to DOCX conversion"""
    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist")
        return
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    print(f"\n4. Testing JSON to DOCX conversion to {JSON_TO_DOCX_URL}")
    response = requests.post(JSON_TO_DOCX_URL, headers=headers, json=json_data)
    
    if response.status_code == 200:
        # Save the DOCX file
        output_file = f"{os.path.splitext(json_file_path)[0]}_converted.docx"
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"✓ Success! DOCX saved to {output_file}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_enhanced_api.py [docx_file_path]")
        sys.exit(1)
    
    docx_file_path = sys.argv[1]
    
    print("=== Testing Enhanced DOCX-to-JSON API Endpoint ===")
    print(f"API Key: {API_KEY}")
    print(f"Testing with file: {docx_file_path}")
    
    # Test all three upload methods
    test_form_upload(docx_file_path)
    test_base64_upload(docx_file_path)
    test_binary_upload(docx_file_path)
    
    # Test JSON to DOCX conversion
    # First get the JSON file from the previous test
    json_file_path = f"{os.path.splitext(docx_file_path)[0]}.json"
    if os.path.exists(json_file_path):
        test_json_to_docx(json_file_path)
    else:
        print("\nSkipping JSON to DOCX test: JSON file not found")
    
    print("\n=== Testing Complete ===")

if __name__ == "__main__":
    main()
