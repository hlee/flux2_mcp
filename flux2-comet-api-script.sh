#!/bin/bash

# Flux Text-to-Image API Script (CometAPI)
# 
# Note: The /flux/v1/ endpoint may not work with all CometAPI keys.
# This script uses the Replicate-compatible endpoint which is confirmed working.
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

echo "🚀 Generating image with Flux via CometAPI..."

# Option 1: Try the direct /flux/v1/ endpoint first (may not work with all keys)
echo "📍 Trying direct /flux/v1/flux-dev endpoint..."
RESPONSE=$(curl -s --location --request POST 'https://api.cometapi.com/flux/v1/flux-dev' \
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

# Check if response is HTML (error) or JSON (success)
if echo "$RESPONSE" | grep -q "<!doctype html>"; then
    echo "⚠️  Direct endpoint not available for this API key"
    echo "📍 Using Replicate-compatible endpoint instead..."
    echo ""
    
    # Option 2: Use Replicate-compatible endpoint (confirmed working)
    RESPONSE=$(curl -s --location --request POST 'https://api.cometapi.com/replicate/v1/models/black-forest-labs/flux-dev/predictions' \
    --header "Authorization: Bearer $COMETAPI_KEY" \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "prompt": "ein fantastisches bild",
            "width": 1024,
            "height": 768,
            "num_outputs": 1,
            "seed": 42
        }
    }')
    
    ENDPOINT_TYPE="replicate"
else
    ENDPOINT_TYPE="direct"
fi

echo "Response: $RESPONSE"
echo ""

# Extract task ID from response (requires jq)
if command -v jq &> /dev/null; then
    TASK_ID=$(echo $RESPONSE | jq -r '.id')
    STATUS=$(echo $RESPONSE | jq -r '.status')
    echo "✅ Task ID: $TASK_ID"
    echo "📊 Initial Status: $STATUS"
    
    echo ""
    echo "⏳ Waiting 5 seconds before checking result..."
    sleep 5
    
    echo "📊 Fetching result..."
    
    if [ "$ENDPOINT_TYPE" = "replicate" ]; then
        # Poll using Replicate endpoint
        RESULT=$(curl -s --location --request GET "https://api.cometapi.com/replicate/v1/predictions/$TASK_ID" \
        --header "Authorization: Bearer $COMETAPI_KEY")
        
        echo "$RESULT" | jq '.'
        
        # Extract image URL if ready
        RESULT_STATUS=$(echo $RESULT | jq -r '.data.status')
        if [ "$RESULT_STATUS" = "SUCCESS" ]; then
            IMAGE_URL=$(echo $RESULT | jq -r '.data.data.output[0]')
            echo ""
            echo "✅ Image generation complete!"
            echo "🖼️  Image URL: $IMAGE_URL"
        else
            echo ""
            echo "⏳ Status: $RESULT_STATUS"
            echo "💡 Try polling again in a few seconds with:"
            echo "curl -s 'https://api.cometapi.com/replicate/v1/predictions/$TASK_ID' \\"
            echo "  --header 'Authorization: Bearer \$COMETAPI_KEY' | jq '.'"
        fi
    else
        # Poll using direct endpoint
        RESULT=$(curl -s --location --request GET "https://api.cometapi.com/flux/v1/get_result?id=$TASK_ID" \
        --header "Authorization: Bearer $COMETAPI_KEY")
        
        echo "$RESULT" | jq '.'
        
        # Extract image URL if ready
        RESULT_STATUS=$(echo $RESULT | jq -r '.status')
        if [ "$RESULT_STATUS" = "Ready" ]; then
            IMAGE_URL=$(echo $RESULT | jq -r '.result.sample')
            echo ""
            echo "✅ Image generation complete!"
            echo "🖼️  Image URL: $IMAGE_URL"
        else
            echo ""
            echo "⏳ Status: $RESULT_STATUS"
            echo "💡 Try polling again in a few seconds with:"
            echo "curl -s 'https://api.cometapi.com/flux/v1/get_result?id=$TASK_ID' \\"
            echo "  --header 'Authorization: Bearer \$COMETAPI_KEY' | jq '.'"
        fi
    fi
else
    echo "⚠️  Install 'jq' to automatically fetch results"
    echo "To check result manually, use one of:"
    echo ""
    echo "# Replicate endpoint:"
    echo "curl -s 'https://api.cometapi.com/replicate/v1/predictions/YOUR_TASK_ID' \\"
    echo "  --header 'Authorization: Bearer \$COMETAPI_KEY'"
    echo ""
    echo "# Direct endpoint:"
    echo "curl -s 'https://api.cometapi.com/flux/v1/get_result?id=YOUR_TASK_ID' \\"
    echo "  --header 'Authorization: Bearer \$COMETAPI_KEY'"
fi
