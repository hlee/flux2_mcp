#!/usr/bin/env python3
"""
Flux API Test Script - CometAPI
Tests image generation and result fetching
"""

import requests
import time
import json
import sys

# Import configuration
try:
    from config import API_KEY, BASE_URL, FLUX_MODEL as MODEL
except ImportError:
    print("❌ Error: config.py not found!")
    print("Please copy config.example.py to config.py and add your API key")
    sys.exit(1)

def generate_image(prompt, width=1024, height=768, seed=42):
    """Generate an image using Flux API"""
    url = f"{BASE_URL}/flux/v1/{MODEL}"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "image_prompt": "",
        "width": width,
        "height": height,
        "prompt_upsampling": False,
        "seed": seed,
        "safety_tolerance": 2,
        "output_format": "jpeg",
        "webhook_url": "",
        "webhook_secret": ""
    }
    
    print(f"🚀 Generating image with prompt: '{prompt}'")
    print(f"📍 URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get("id")
            print(f"✅ Task created successfully!")
            print(f"🆔 Task ID: {task_id}")
            return task_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def get_result(task_id, max_attempts=30, poll_interval=2):
    """Poll for image generation result"""
    url = f"{BASE_URL}/flux/v1/get_result"
    
    headers = {
        "Authorization": API_KEY
    }
    
    params = {
        "id": task_id
    }
    
    print(f"\n⏳ Polling for results (Task ID: {task_id})")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                
                print(f"📊 Attempt {attempt + 1}/{max_attempts} - Status: {status}")
                
                if status == "Ready":
                    print(f"\n✅ Image generation complete!")
                    result = data.get("result", {})
                    image_url = result.get("sample")
                    duration = result.get("duration")
                    
                    print(f"🖼️  Image URL: {image_url}")
                    print(f"⏱️  Duration: {duration}s")
                    print(f"🌱 Seed: {result.get('seed')}")
                    
                    return data
                    
                elif status in ["Error", "Failed"]:
                    print(f"❌ Generation failed: {data}")
                    return None
                    
                else:
                    time.sleep(poll_interval)
                    
            else:
                print(f"❌ Error polling: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Exception while polling: {e}")
            return None
    
    print(f"⏰ Timeout: Max attempts reached")
    return None

def main():
    """Main execution"""
    print("=" * 60)
    print("Flux API Test - CometAPI")
    print("=" * 60)
    
    # Test with a simple prompt
    prompt = "a beautiful sunset over mountains, photorealistic"
    
    # Step 1: Generate image
    task_id = generate_image(prompt)
    
    if not task_id:
        print("\n❌ Failed to create generation task")
        sys.exit(1)
    
    # Step 2: Poll for result
    result = get_result(task_id)
    
    if result:
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Test failed")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
