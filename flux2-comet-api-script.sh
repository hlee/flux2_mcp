#!/bin/bash

# Flux 2 Text-to-Image API Script (Comet API)
# Model: flux-2-flex
#
# Usage:
#   export COMETAPI_KEY="your-api-key-here"
#   ./flux2-comet-api-script.sh

# Check if API key is set
if [ -z "$COMETAPI_KEY" ]; then
    echo "❌ Error: COMETAPI_KEY environment variable is not set"
    echo "Please set it with: export COMETAPI_KEY='your-api-key-here'"
    exit 1
fi

echo "🚀 Generating image with Flux 2..."

# Generate image
RESPONSE=$(curl --location --request POST 'https://api.cometapi.com/flux/v1/flux-2-flex' \
--header "Authorization: $COMETAPI_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
    "prompt": "ein fantastisches bild",
    "image_prompt": "",
    "width": 1024,
    "height": 768,
    "prompt_upsampling": false,
    "seed": 42,
    "safety_tolerance": 2,
    "output_format": "jpeg",
    "webhook_url": "",
    "webhook_secret": ""
}')

echo "Response: $RESPONSE"

# Extract task ID from response (requires jq)
if command -v jq &> /dev/null; then
    TASK_ID=$(echo $RESPONSE | jq -r '.id')
    echo "✅ Task ID: $TASK_ID"
    
    echo ""
    echo "⏳ Waiting 5 seconds before checking result..."
    sleep 5
    
    echo "📊 Fetching result..."
    curl --location --request GET "https://api.cometapi.com/flux/v1/get_result?id=$TASK_ID" \
    --header "Authorization: Bearer $COMETAPI_KEY"
else
    echo "⚠️  Install 'jq' to automatically fetch results"
    echo "To check result manually, use:"
    echo "curl --location --request GET 'https://api.cometapi.com/flux/v1/get_result?id=YOUR_TASK_ID' \\"
    echo "--header 'Authorization: Bearer \$COMETAPI_KEY'"
fi
