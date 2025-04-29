#!/bin/bash

# API endpoint - Corrected URL format for Hugging Face Spaces
API_URL="https://obijuancodenobi-docgen.hf.space/api/json-to-docx"

# API key from .env file
source .env
API_KEY="${API_KEY:-docgen_api_12345}"

echo "Using API key: $API_KEY"
echo "Sending request to: $API_URL"

# Send the request
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d @test_document.json \
  --output converted_document.docx

# Check if the request was successful
if [ -f "converted_document.docx" ]; then
  echo "Success! DOCX file saved as 'converted_document.docx'"
  # Get file size
  file_size=$(du -h converted_document.docx | cut -f1)
  echo "File size: $file_size"
else
  echo "Error: Failed to save DOCX file"
fi
