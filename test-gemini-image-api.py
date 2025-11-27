#!/usr/bin/env python3
"""
Gemini Image Generation Test Script - CometAPI
Tests text-to-image and image-to-image generation using Gemini models
"""

import requests
import base64
import json
import sys
from pathlib import Path

# Import configuration
try:
    from config import API_KEY, BASE_URL, GEMINI_MODEL as MODEL
except ImportError:
    print("❌ Error: config.py not found!")
    print("Please copy config.example.py to config.py and add your API key")
    sys.exit(1)

def generate_image_from_text(prompt, aspect_ratio="1:1", output_file="output.png"):
    """Generate an image from text prompt using Gemini"""
    url = f"{BASE_URL}/v1beta/models/{MODEL}:generateContent"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"],  # Force image output only
            "aspectRatio": aspect_ratio
        }
    }
    
    print(f"🚀 Generating image from text prompt")
    print(f"📝 Prompt: '{prompt}'")
    print(f"📐 Aspect Ratio: {aspect_ratio}")
    print(f"📍 URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract image from response
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                
                for part in parts:
                    if "inlineData" in part or "inline_data" in part:
                        inline_data = part.get("inlineData") or part.get("inline_data")
                        mime_type = inline_data.get("mimeType") or inline_data.get("mime_type")
                        image_data = inline_data.get("data")
                        
                        if image_data:
                            # Decode and save image
                            image_bytes = base64.b64decode(image_data)
                            
                            # Determine file extension from mime type
                            ext_map = {
                                "image/png": ".png",
                                "image/jpeg": ".jpg",
                                "image/jpg": ".jpg",
                                "image/webp": ".webp"
                            }
                            ext = ext_map.get(mime_type, ".png")
                            output_path = Path(output_file).with_suffix(ext)
                            
                            with open(output_path, "wb") as f:
                                f.write(image_bytes)
                            
                            print(f"✅ Image generated successfully!")
                            print(f"💾 Saved to: {output_path}")
                            print(f"📦 Size: {len(image_bytes)} bytes")
                            print(f"🎨 MIME Type: {mime_type}")
                            return str(output_path)
                
                print("❌ No image data found in response")
                print(f"Response: {json.dumps(data, indent=2)[:500]}")
            else:
                print("❌ No candidates in response")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    return None

def generate_image_from_image(prompt, input_image_path, output_file="output_modified.png"):
    """Generate an image from text + input image using Gemini"""
    url = f"{BASE_URL}/v1beta/models/{MODEL}:generateContent"
    
    # Read and encode input image
    try:
        with open(input_image_path, "rb") as f:
            image_bytes = f.read()
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        print(f"❌ Failed to read input image: {e}")
        return None
    
    # Determine mime type
    ext = Path(input_image_path).suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp"
    }
    mime_type = mime_map.get(ext, "image/jpeg")
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    },
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_b64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }
    
    print(f"🚀 Generating image from text + image")
    print(f"📝 Prompt: '{prompt}'")
    print(f"🖼️  Input Image: {input_image_path}")
    print(f"📍 URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract image from response
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                
                for part in parts:
                    if "inlineData" in part or "inline_data" in part:
                        inline_data = part.get("inlineData") or part.get("inline_data")
                        mime_type = inline_data.get("mimeType") or inline_data.get("mime_type")
                        image_data = inline_data.get("data")
                        
                        if image_data:
                            # Decode and save image
                            image_bytes = base64.b64decode(image_data)
                            
                            ext_map = {
                                "image/png": ".png",
                                "image/jpeg": ".jpg",
                                "image/jpg": ".jpg",
                                "image/webp": ".webp"
                            }
                            ext = ext_map.get(mime_type, ".png")
                            output_path = Path(output_file).with_suffix(ext)
                            
                            with open(output_path, "wb") as f:
                                f.write(image_bytes)
                            
                            print(f"✅ Image generated successfully!")
                            print(f"💾 Saved to: {output_path}")
                            print(f"📦 Size: {len(image_bytes)} bytes")
                            return str(output_path)
                
                print("❌ No image data found in response")
            else:
                print("❌ No candidates in response")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    return None

def main():
    """Main execution"""
    print("=" * 70)
    print("Gemini Image Generation Test - CometAPI")
    print(f"Model: {MODEL}")
    print("=" * 70)
    
    # Test 1: Text-to-Image
    print("\n📝 Test 1: Text-to-Image Generation")
    print("-" * 70)
    prompt = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
    result = generate_image_from_text(prompt, aspect_ratio="16:9", output_file="gemini_text_output.png")
    
    if result:
        print(f"\n✅ Test 1 passed: {result}")
    else:
        print("\n❌ Test 1 failed")
    
    # Test 2: Image-to-Image (only if you have an input image)
    # Uncomment the following to test image-to-image generation:
    """
    print("\n\n🖼️  Test 2: Image-to-Image Generation")
    print("-" * 70)
    input_image = "input.jpg"  # Replace with your image path
    prompt2 = "Make this image more vibrant and add a sunset background"
    result2 = generate_image_from_image(prompt2, input_image, "gemini_image_output.png")
    
    if result2:
        print(f"\n✅ Test 2 passed: {result2}")
    else:
        print("\n❌ Test 2 failed")
    """
    
    print("\n" + "=" * 70)
    print("✅ Testing completed!")
    print("=" * 70)

if __name__ == "__main__":
    main()
