#!/usr/bin/env python3
"""
Test script for the JSON to DOCX API endpoint on Railway
"""

import requests
import json
import os
import sys
import argparse

# API endpoint URL
BASE_URL = "https://docgen-production-3242.up.railway.app"
JSON_TO_DOCX_URL = f"{BASE_URL}/api/json-to-docx"

# API key from .env file or use the default one from memory
API_KEY = os.environ.get('API_KEY', 'docgen_api_12345')

def test_json_to_docx(json_file_path, output_file=None):
    """Test the JSON to DOCX conversion on the Railway deployment"""
    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist")
        return
    
    # Set default output file name if not provided
    if output_file is None:
        output_file = f"{os.path.splitext(json_file_path)[0]}_railway.docx"
    
    headers = {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    print(f"Testing JSON to DOCX conversion on {JSON_TO_DOCX_URL}")
    print(f"Using API Key: {API_KEY}")
    
    try:
        response = requests.post(JSON_TO_DOCX_URL, headers=headers, json=json_data, timeout=30)
        
        if response.status_code == 200:
            # Save the DOCX file
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"✓ Success! DOCX saved to {output_file}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def create_sample_json():
    """Create a sample JSON file for testing"""
    sample_json = {
        "document": {
            "blocks": [
                {
                    "type": "heading",
                    "level": 1,
                    "runs": [
                        {
                            "text": "Railway API Test Document",
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
                            "text": "This is a test document created to test the Railway deployment of the Document Format Converter API.",
                            "bold": False,
                            "italic": False,
                            "underline": False
                        }
                    ]
                },
                {
                    "type": "heading",
                    "level": 2,
                    "runs": [
                        {
                            "text": "Text Formatting",
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
                            "text": "This paragraph contains ",
                            "bold": False,
                            "italic": False,
                            "underline": False
                        },
                        {
                            "text": "bold",
                            "bold": True,
                            "italic": False,
                            "underline": False
                        },
                        {
                            "text": ", ",
                            "bold": False,
                            "italic": False,
                            "underline": False
                        },
                        {
                            "text": "italic",
                            "bold": False,
                            "italic": True,
                            "underline": False
                        },
                        {
                            "text": ", and ",
                            "bold": False,
                            "italic": False,
                            "underline": False
                        },
                        {
                            "text": "underlined",
                            "bold": False,
                            "italic": False,
                            "underline": True
                        },
                        {
                            "text": " text.",
                            "bold": False,
                            "italic": False,
                            "underline": False
                        }
                    ]
                },
                {
                    "type": "heading",
                    "level": 2,
                    "runs": [
                        {
                            "text": "Conclusion",
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
                            "text": "If this document is successfully converted to DOCX format, the API is working correctly.",
                            "bold": False,
                            "italic": False,
                            "underline": False
                        }
                    ]
                }
            ]
        }
    }
    
    sample_file = "railway_test.json"
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump(sample_json, f, indent=2)
    
    print(f"Created sample JSON file: {sample_file}")
    return sample_file

def main():
    parser = argparse.ArgumentParser(description="Test the JSON to DOCX API endpoint on Railway")
    parser.add_argument("--json", help="Path to JSON file (if not provided, a sample will be created)")
    parser.add_argument("--output", help="Path to output DOCX file")
    parser.add_argument("--api-key", help="API key to use (default: docgen_api_12345)")
    
    args = parser.parse_args()
    
    if args.api_key:
        global API_KEY
        API_KEY = args.api_key
    
    json_file = args.json if args.json else create_sample_json()
    output_file = args.output
    
    test_json_to_docx(json_file, output_file)

if __name__ == "__main__":
    main()
