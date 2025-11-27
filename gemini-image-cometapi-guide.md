# Guide to calling gemini-3-pro-image (Nano Banana)

This document demonstrates how to use Google Gemini's image model, `gemini-3-pro-image`, via cometapi for image generation. It covers two common methods:
- Gemini's official `generateContent` API for text-to-image generation
- Gemini's official `generateContent` API for image-to-image generation (both input and output are Base64)

**Important Notes:**
- Replace `sk-xxxx` in the examples with your cometapi key. For security, do not expose your key in client-side code or public repositories.
- The `Authorization` header for cometapi typically uses the key value directly, e.g., `Authorization: sk-xxxx`.
- The returned image is usually provided as Base64-encoded `inline_data`. You will need to decode it on the client side and save it as a file.

**Basic Information:**
- **Base URL:** `https://api.cometapi.com`
- **Model Name:** `gemini-3-pro-image` / `gemini-2.5-flash-image`

----------------------------------------

## I. Gemini's Official `generateContent` for Text-to-Image

Use Gemini's official `generateContent` endpoint for text-to-image generation. Place the text prompt in `contents.parts[].text`.

**Example (Windows shell, using `^` for line continuation):**
```shell
curl --location --request POST "https://api.cometapi.com/v1beta/models/gemini-3-pro-image:generateContent" ^
--header "Authorization: sk-xxxx" ^
--header "User-Agent: Apifox/1.0.0 (https://apifox.com)" ^
--header "Content-Type: application/json" ^
--header "Accept: */*" ^
--header "Host: api.cometapi.com" ^
--header "Connection: keep-alive" ^
--data-raw "{    \"contents\": [{      \"parts\": [        {\"text\": \"Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme\"}      ]    }]  }"
```

**Response Highlights:**
- The image data is typically found in `response.candidates[0].content.parts`, which can contain:
  - Text description:
    ```json
    { "text": "..." }
    ```
  - Image data:
    ```json
    { "inline_data": { "mime_type": "image/png", "data": "<base64>" } }
    ```
- Decode the `data` field (the Base64 string) and save it as a file with the corresponding extension.

----------------------------------------

## II. Gemini's Official `generateContent` for Image-to-Image (Base64 I/O)

This endpoint supports "image-to-image" generation: upload an input image (as Base64) and receive a modified new image (also in Base64 format).

**Example:**

```js
curl --location --request POST 'https://api.cometapi.com/v1beta/models/gemini-3-pro-image:generateContent' \
--header 'Authorization: sk-xxx' \
--header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--header 'Host: api.cometapi.com' \
--header 'Connection: keep-alive' \
--data-raw '{
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": "cat"
                },
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
						"data": "iVBORw0KGgoA Note: Base64 data here"
						}
       
            ]
        }
    ],
    "generationConfig": {
        "responseModalities": [
            "TEXT",
            "IMAGE"
        ]
    }
}'
```


**Description:**
- First, convert your source image file into a Base64 string and place it in `inline_data.data`. Do not include prefixes like `data:image/jpeg;base64,`.
- The output is also located in `candidates[0].content.parts` and includes:
  - An optional text part (description or prompt).
  - The image part as `inline_data` (where `data` is the Base64 of the output image).
  - For multiple images, you can append them directly, for example:

```js
{
"inline_data": 
   {
   "mime_type": "image/jpeg",
   "data": "iVBORw0KGgo..."
   }
},
{
"inline_data": 
   {
   "mime_type": "image/jpeg",
   "data": "iVBORw0KGgo..."
   }
}
```
---------------------------------------

## III. Official Gemini: Image Generation from Multiple Images (Base64 Input/Output)

This endpoint supports "multi-image to image" generation: upload multiple input images (Base64) and it will return a new, modified image (also in Base64 format).
### Method 1: Combine multiple images into a single collage, as shown in the example below
![99002da7909de23682b9390cf1b325a0.jpg](https://api.apifox.com/api/v1/projects/6100640/resources/569419/image-preview)
- Example input description:
- A model is posing and leaning against a pink bmw. She is wearing the following items, the scene is against a light grey background. The green alien is a keychain and it's attached to the pink handbag. The model also has a pink parrot on her shoulder. There is a pug sitting next to her wearing a pink collar and gold headphones.

- Returned Base64 converted back to an image:
![68774664ff156db0ee5d50861b620932.jpg](https://api.apifox.com/api/v1/projects/6100640/resources/569420/image-preview)

- Example:
```
curl --location --request POST 'https://api.cometapi.com/v1beta/models/gemini-3-pro-image:generateContent' \
--header 'Authorization: sk-xxx' \
--header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--header 'Host: api.cometapi.com' \
--header 'Connection: keep-alive' \
--data-raw '{
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": "A model is posing and leaning against a pink bmw. She is wearing the following items, the scene is against a light grey background. The green alien is a keychain and it's attached to the pink handbag. The model also has a pink parrot on her shoulder. There is a pug sitting next to her wearing a pink collar and gold headphones"
                },
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
						"data": "iVBORw0KGgoA Note: Base64 data here"
						}
       
            ]
        }
    ],
    "generationConfig": {
        "responseModalities": [
            "TEXT",
            "IMAGE"
        ]
    }
}'
```

Notes:
- First, convert your source image file to a Base64 string and insert it into `inline_data.data` (do not include prefixes like `data:image/jpeg;base64,`).
- The output is also located in `candidates[0].content.parts` and contains:
  - An optional text part (description or prompt)
  - An image part `inline_data` (where `data` is the Base64 of the output image)
### Method 2: Pass multiple images via Base64 parameters (up to three images)
- Example:

```js
curl --location --request POST 'https://api.cometapi.com/v1beta/models/gemini-3-pro-image:generateContent' \
--header 'Authorization: sk-xxx' \
--header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--header 'Host: api.cometapi.com' \
--header 'Connection: keep-alive' \
--data-raw '{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Merge the three images"
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
			"data": "iVBORw0KGgoA Note: Base64 data here"
          }
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
			"data": "iVBORw0KGgoA Note: Base64 data here"
          }
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
			"data": "iVBORw0KGgoA Note: Base64 data here"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": [
      "TEXT",
      "IMAGE"
    ]
  }
}'
```
- API Input Parameters:

```js
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Merge the three images"
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
			"data": "UklGRlZvAABXRUJQVlA4TElvAAAvz..." 
         
		  }
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
			"data": "UklGRlZvAABXRUJQVlA4TElvAAAvz..." 
			}
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
			"data": "UklGRlZvAABXRUJQVlA4TElvAAAvz..." 
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": [
      "TEXT",
      "IMAGE"
    ]
  }
}
```
- Example of returned image:

![converted_image.png](https://api.apifox.com/api/v1/projects/6100640/resources/569429/image-preview)

## How to Extract and Save the Base64 Image from the Response

Using the Gemini-style response as an example, the pseudo-structure is as follows (for illustration purposes):
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          { "text": "..." },
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "<base64-string>"
            }
          }
        ]
      }
    }
  ]
}
```

- Extract the `inlineData.data` string and choose the file extension based on its `mimeType` (e.g., `.png`, `.jpg`, `.webp`).
- In your client application, decode the Base64 string and save it as a binary file.

**Python Example:**
```python
import base64

b64_string = "<base64-string>"
with open("output.png", "wb") as f:
    f.write(base64.b64decode(b64_string))
```

**Node.js Example:**
```javascript
const fs = require("fs");

const b64_string = "<base64-string>";
fs.writeFileSync("output.png", Buffer.from(b64_string, "base64"));
```

----------------------------------------

## FAQ & Suggestions

- **Authorization Header Format**
  - Use `Authorization: sk-xxxx`. Please refer to the official cometapi documentation for confirmation.
- **Prompt Optimization**
  - Specifying style keywords (e.g., "cyberpunk, film grain, low contrast, high saturation"), aspect ratio (square/landscape/portrait), subject, background, lighting, and level of detail can help improve the results.
- **Base64 Note**
  - Do not include a prefix like `data:image/png;base64,` in the `data` field; only include the pure Base64 data string.
- **Troubleshooting**
  - `4xx` errors usually indicate issues with request parameters or authentication (check your key, model name, JSON format). `5xx` errors are server-side problems (you can retry later or contact support).

The above covers the methods and key points for using `gemini-3-pro-image` via cometapi. Choose the API style that suits your needs and implement the Base64 image decoding and display on the client side.
- ## 🍌 Flash 2.5 Image Updates

### a. Flexible Aspect Ratios
Now supports multiple aspect ratio settings for easy content creation across different devices. All resolutions consume 1,290 tokens by default.

**Supported aspect ratios:**
1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

**Reference examples:**
- https://ai.google.dev/gemini-api/docs/image-generation#aspect_ratios
- https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation#googlegenaisdk_imggen_mmflash_with_txt-drest
- https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/getting-started/intro_gemini_2_5_image_gen.ipynb

### b. Model Name Update
All new features will be available on the new model ID: **`gemini-2.5-flash-image`**. The previous `preview` will be deprecated.

⚠️ **Migration required by October 31, 2025**

### c. Force Image Output
To address the frequent issue of text-only outputs, you can now set `"responseModalities"` to `["IMAGE"]` only in API requests. This ensures image generation without text-only responses.
**Official API documentation for reference:**
- [Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Image Understanding (Multimodal)](https://ai.google.dev/gemini-api/docs/image-understanding)
- [Image Generation](https://ai.google.dev/gemini-api/docs/image-generation?hl=zh-cn#image_generation_text-to-image)
Explain