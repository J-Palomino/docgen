import requests
import os
import sys
import json

# API endpoint URLs
BASE_URL = "http://localhost:8000"  # Flask runs on port 8000 by default
DOCX_TO_JSON_URL = f"{BASE_URL}/api/docx-to-json"
JSON_TO_DOCX_URL = f"{BASE_URL}/api/json-to-docx"

# API key from .env file or use the default one from memory
API_KEY = os.environ.get('API_KEY', 'docgen_api_12345')

def test_docx_to_json(docx_file_path):
    """Test the DOCX to JSON conversion API endpoint"""
    if not os.path.exists(docx_file_path):
        print(f"Error: File {docx_file_path} does not exist")
        return
    
    headers = {
        'X-API-Key': API_KEY
    }
    
    with open(docx_file_path, 'rb') as f:
        files = {'file': (os.path.basename(docx_file_path), f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
        print(f"Sending request to {DOCX_TO_JSON_URL} with API key: {API_KEY}")
        response = requests.post(DOCX_TO_JSON_URL, headers=headers, files=files)
    
    if response.status_code == 200:
        # Save the JSON response to a file
        output_file = f"{os.path.splitext(docx_file_path)[0]}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=2)
        print(f"Success! JSON saved to {output_file}")
        print("First 500 characters of the JSON response:")
        print(json.dumps(response.json(), indent=2)[:500] + "...")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_json_to_docx(json_file_path):
    """Test the JSON to DOCX conversion API endpoint"""
    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist")
        return
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    print(f"Sending request to {JSON_TO_DOCX_URL} with API key: {API_KEY}")
    response = requests.post(JSON_TO_DOCX_URL, headers=headers, json=json_data)
    
    if response.status_code == 200:
        # Save the DOCX response to a file
        output_file = f"{os.path.splitext(json_file_path)[0]}_converted.docx"
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Success! DOCX saved to {output_file}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    if len(sys.argv) < 3:
        print("Usage: python test_api.py [docx-to-json|json-to-docx] [file_path]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    file_path = sys.argv[2]
    
    if command == "docx-to-json":
        test_docx_to_json(file_path)
    elif command == "json-to-docx":
        test_json_to_docx(file_path)
    else:
        print(f"Unknown command: {command}")
        print("Usage: python test_api.py [docx-to-json|json-to-docx] [file_path]")
        sys.exit(1)

if __name__ == "__main__":
    main()
