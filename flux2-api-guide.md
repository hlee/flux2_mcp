# FLUX.2 Text-to-Image API Usage

Generate high-fidelity images with FLUX.2, featuring photorealism, accurate hands/faces, flexible aspect ratios, and exact color steering (hex codes). Choose between:
- FLUX.2 [pro]: fast, efficient, production-friendly
- FLUX.2 [flex]: maximum quality with adjustable steps/guidance

## Prerequisites
- Create an account and obtain an API key from the BFL Dashboard.
- Set your API key in the `x-key` request header.

## Endpoints
- POST `https://api.bfl.ai/v1/flux-2-pro` — FLUX.2 [pro]
- POST `https://api.bfl.ai/v1/flux-2-flex` — FLUX.2 [flex]
- GET  `https://api.bfl.ai/v1/get_result?id=<task_id>` — Polling for results

## Request: Create a Generation

### cURL (pro)
```bash
curl -X POST https://api.bfl.ai/v1/flux-2-pro \
  -H 'accept: application/json' \
  -H "x-key: $BFL_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Cinematic shot of a futuristic city at sunset, 85mm lens",
    "width": 1920,
    "height": 1080,
    "safety_tolerance": 2
  }'
```

### cURL (flex)
```bash
curl -X POST https://api.bfl.ai/v1/flux-2-flex \
  -H 'accept: application/json' \
  -H "x-key: $BFL_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Clean poster layout with bold typography in #FF5733 and #1E90FF",
    "width": 2048,
    "height": 2048,
    "safety_tolerance": 2,
    "steps": 50,
    "guidance": 4.5,
    "output_format": "png"
  }'
```

### Python (requests)
```python
import requests

API_KEY = "YOUR_BFL_API_KEY"
HEADERS = {
    "accept": "application/json",
    "x-key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "prompt": "Cinematic shot of a futuristic city at sunset, 85mm lens",
    "width": 1920,
    "height": 1080,
    "safety_tolerance": 2,
    # flex-only:
    # "steps": 50,
    # "guidance": 4.5,
    # "output_format": "png",
}

# Choose pro or flex:
resp = requests.post("https://api.bfl.ai/v1/flux-2-pro", headers=HEADERS, json=payload)
resp.raise_for_status()
data = resp.json()

print("Task ID:", data["id"])
print("Polling URL:", data["polling_url"])
print("Cost (credits):", data.get("cost"))
print("Output MP:", data.get("output_mp"))
```

## Response (Submission)
The initial response confirms task creation and pricing:
```json
{
  "id": "task-id-here",
  "polling_url": "https://api.bfl.ai/v1/get_result?id=task-id-here",
  "cost": 3.0,
  "input_mp": 0.0,
  "output_mp": 2.07
}
```

- `cost`: credits charged for the request
- `output_mp`: megapixels of generated output

## Retrieve Results (Polling)

### cURL
```bash
curl -X GET "$POLLING_URL" \
  -H 'accept: application/json' \
  -H "x-key: $BFL_API_KEY"
```

Poll until `status` is `Ready`. Then the response includes image data/URL(s) depending on your integration.

### Python
```python
import time, requests

polling_url = data["polling_url"]

while True:
    r = requests.get(polling_url, headers={"accept":"application/json","x-key":API_KEY})
    r.raise_for_status()
    result = r.json()
    status = result.get("status")
    if status == "Ready":
        print("Result:", result)
        # Save image if the API returns a URL or base64 content
        # e.g., download via requests.get(result["images"][0]["url"])
        break
    elif status in ("Error", "Failed"):
        raise RuntimeError(f"Generation failed: {result}")
    else:
        time.sleep(1.5)
```

## Parameters

### Common
- `prompt` (string, required): description of the image.
- `width` (int, default 1024): output width in pixels. Must be a multiple of 16.
- `height` (int, default 1024): output height in pixels. Must be a multiple of 16.
- `seed` (int, default random): set for reproducible results.
- `safety_tolerance` (int, default 2): moderation level, range 0–6. Lower = stricter.
- `output_format` (string, default `"jpeg"`): `"jpeg"` or `"png"`.

### FLUX.2 [flex]-only
- `steps` (int, default 50, max 50): inference steps. Higher = more detail, slower.
- `guidance` (float, default 4.5, min 1.5, max 10): prompt adherence. Higher = closer to prompt.

### Resolution Limits
- Minimum: 64×64
- Maximum: up to 4MP (e.g., 2048×2048)
- Dimensions must be multiples of 16
- Recommended: up to 2MP for performance

## Model Selection

| Model | Best for | Speed | Controls | Pricing |
|------|----------|-------|----------|---------|
| FLUX.2 [pro] | Production workflows, fast turnaround | < 10s | Standard | ~$0.03/image |
| FLUX.2 [flex] | Highest detail & adherence | Higher latency | Adjustable `steps` & `guidance` | ~$0.06/image |

Note: Pricing shown for reference; check your dashboard for current rates.

## Error Handling
- Validate dimensions (multiples of 16; within limits).
- Handle moderation responses via `safety_tolerance`.
- Implement retry/backoff on polling to respect rate limits.
- Check `status` for `Ready`, `Error`, or `Failed`.

## Examples

### Photorealistic Portrait (pro)
```bash
curl -X POST https://api.bfl.ai/v1/flux-2-pro \
  -H 'accept: application/json' \
  -H "x-key: $BFL_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Photorealistic portrait, soft rim lighting, natural skin texture, color-accurate background #1E90FF",
    "width": 1536,
    "height": 2048,
    "safety_tolerance": 2
  }'
```

### Typography & Design with Hex Colors (flex)
```bash
curl -X POST https://api.bfl.ai/v1/flux-2-flex \
  -H 'accept: application/json' \
  -H "x-key: $BFL_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Clean layout poster: headline in #FF5733, subheading in #1E90FF, body text in #222222, grid-based composition, balanced white space",
    "width": 2048,
    "height": 2048,
    "steps": 50,
    "guidance": 5.5,
    "output_format": "png",
    "safety_tolerance": 2
  }'
```

## Tips
- Use `seed` for reproducibility when iterating designs.
- For speed-critical flows, start with [pro]; switch to [flex] for final assets.
- Keep aspect ratios close to your target use-case (e.g., 1:1 for social, 16:9 for banners).
- Monitor `cost` in responses to manage credits.

## Compliance
Review BFL’s Terms of Use, Usage Policy, and Responsible AI Development Policy before deploying.

