# Flux API Guide - CometAPI

## Overview

CometAPI provides access to Flux text-to-image generation models. This guide covers the endpoints, parameters, and usage patterns for generating images programmatically.

## Base URL

```
https://api.cometapi.com
```

## Authentication

All requests require an API key passed in the `Authorization` header:

```
Authorization: Bearer {your-api-key}
```

Or without Bearer prefix:

```
Authorization: {your-api-key}
```

## Supported Models

- `flux-pro-1.1-ultra`
- `flux-pro-1.1`
- `flux-pro`
- `flux-dev`
- `flux-pro-1.0-fill`
- `flux-pro-1.0-canny`
- `flux-pro-1.0-depth`
- `flux-kontext-pro`
- `flux-kontext-max`
- `flux-2-pro`
- `flux-2-flex`

## Endpoints

### 1. Generate Image

**Endpoint:** `POST /flux/v1/{model}`

Generate an image based on a text prompt.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| model | string | Yes | Model name (e.g., `flux-2-flex`) |

#### Headers

| Header | Value | Required |
|--------|-------|----------|
| Authorization | Bearer {api-key} | Yes |
| Content-Type | application/json | Yes |

#### Request Body

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| prompt | string | Yes | - | Text description of the image to generate |
| image_prompt | string | No | "" | Optional image URL for image-to-image generation |
| width | integer | No | 1024 | Image width in pixels |
| height | integer | No | 768 | Image height in pixels |
| prompt_upsampling | boolean | No | false | Enable automatic prompt enhancement |
| seed | integer | No | random | Random seed for reproducible results |
| safety_tolerance | integer | No | 2 | Content moderation level (0-6, lower = stricter) |
| output_format | string | No | "jpeg" | Output format: `jpeg`, `png`, or `webp` |
| webhook_url | string | No | "" | URL to receive completion notification |
| webhook_secret | string | No | "" | Secret for webhook authentication |

#### Example Request

```bash
curl --location --request POST 'https://api.cometapi.com/flux/v1/flux-2-flex' \
--header 'Authorization: YOUR_API_KEY_HERE' \
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
}'
```

#### Response

```json
{
  "id": "1n6vvx3ykhrm80cphgnafcmvgg",
  "status": "Pending"
}
```

### 2. Get Result

**Endpoint:** `GET /flux/v1/get_result`

Query the status and result of an image generation task.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Task ID returned from generation request |

#### Headers

| Header | Value | Required |
|--------|-------|----------|
| Authorization | Bearer {api-key} | Yes |

#### Example Request

```bash
curl --location --request GET 'https://api.cometapi.com/flux/v1/get_result?id=1n6vvx3ykhrm80cphgnafcmvgg' \
--header 'Authorization: Bearer YOUR_API_KEY_HERE'
```

#### Response (Pending)

```json
{
  "id": "1n6vvx3ykhrm80cphgnafcmvgg",
  "status": "Pending"
}
```

#### Response (Ready)

```json
{
  "id": "a8b95720-6eb2-4ef2-b120-2a1b99d41324",
  "result": {
    "seed": 42,
    "prompt": "ein fantastisches bild",
    "sample": "https://bfldeliverysc.blob.core.windows.net/...",
    "duration": 5.063358545303345,
    "end_time": 1731467769.3061166,
    "start_time": 1731467764.242758
  },
  "status": "Ready"
}
```

#### Status Values

- `Pending` - Task is queued or processing
- `Ready` - Generation complete, image available
- `Error` - Generation failed
- `Failed` - Task failed

## Compatibility

The `/flux/v1/get_result` endpoint is also compatible with tasks created via:
- `/replicate/v1/models/{model}/predictions`
- `/flux/v1/{model}`

## Usage Workflow

1. **Submit Generation Request**
   - POST to `/flux/v1/{model}` with your prompt and parameters
   - Receive task ID in response

2. **Poll for Results**
   - GET `/flux/v1/get_result?id={task_id}`
   - Check `status` field
   - When status is `Ready`, retrieve image from `result.sample` URL

3. **Download Image**
   - Use the URL from `result.sample` to download the generated image

## Code Examples

### Python

```python
import requests
import time

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.cometapi.com"

# Step 1: Generate image
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "ein fantastisches bild",
    "width": 1024,
    "height": 768,
    "seed": 42,
    "safety_tolerance": 2,
    "output_format": "jpeg"
}

response = requests.post(
    f"{BASE_URL}/flux/v1/flux-2-flex",
    headers=headers,
    json=payload
)
task_id = response.json()["id"]
print(f"Task ID: {task_id}")

# Step 2: Poll for result
while True:
    result = requests.get(
        f"{BASE_URL}/flux/v1/get_result",
        headers=headers,
        params={"id": task_id}
    )
    data = result.json()
    status = data["status"]
    
    if status == "Ready":
        image_url = data["result"]["sample"]
        print(f"Image ready: {image_url}")
        break
    elif status in ["Error", "Failed"]:
        print(f"Generation failed: {data}")
        break
    
    time.sleep(2)
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_KEY = 'YOUR_API_KEY_HERE';
const BASE_URL = 'https://api.cometapi.com';

async function generateImage() {
  // Step 1: Generate image
  const response = await axios.post(
    `${BASE_URL}/flux/v1/flux-2-flex`,
    {
      prompt: 'ein fantastisches bild',
      width: 1024,
      height: 768,
      seed: 42,
      safety_tolerance: 2,
      output_format: 'jpeg'
    },
    {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  const taskId = response.data.id;
  console.log(`Task ID: ${taskId}`);
  
  // Step 2: Poll for result
  while (true) {
    const result = await axios.get(
      `${BASE_URL}/flux/v1/get_result`,
      {
        headers: { 'Authorization': `Bearer ${API_KEY}` },
        params: { id: taskId }
      }
    );
    
    const { status, result: imageResult } = result.data;
    
    if (status === 'Ready') {
      console.log(`Image ready: ${imageResult.sample}`);
      return imageResult.sample;
    } else if (status === 'Error' || status === 'Failed') {
      throw new Error(`Generation failed: ${JSON.stringify(result.data)}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

generateImage().catch(console.error);
```

## Best Practices

1. **Polling Interval**: Poll every 2-3 seconds to avoid rate limiting
2. **Timeout Handling**: Implement a maximum polling duration (e.g., 5 minutes)
3. **Error Handling**: Check for `Error` and `Failed` status values
4. **Seed Usage**: Use consistent seed values for reproducible results
5. **Webhooks**: For production, use webhooks instead of polling for better efficiency

## Rate Limits

Check CometAPI documentation for current rate limits and pricing information.

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid API key |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

## Support

For API support and documentation updates, refer to the [official CometAPI documentation](https://api.cometapi.com).
