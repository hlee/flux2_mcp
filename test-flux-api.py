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
    """Generate an image using Flux API via Replicate endpoint"""
    # Use Replicate-compatible endpoint which works with CometAPI
    url = f"{BASE_URL}/replicate/v1/models/black-forest-labs/{MODEL}/predictions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_outputs": 1,
            "seed": seed
        }
    }
    
    print(f"🚀 Generating image with prompt: '{prompt}'")
    print(f"📍 URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            task_id = data.get("id")
            print(f"✅ Task created successfully!")
            print(f"🆔 Task ID: {task_id}")
            print(f"📄 Status: {data.get('status')}")
            return task_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def get_result(task_id, max_attempts=30, poll_interval=2):
    """Poll for image generation result using Replicate endpoint"""
    url = f"{BASE_URL}/replicate/v1/predictions/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print(f"\n⏳ Polling for results (Task ID: {task_id})")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle CometAPI response format
                if "data" in data and "status" in data["data"]:
                    status = data["data"]["status"]
                    progress = data["data"].get("progress", "")
                    
                    print(f"📊 Attempt {attempt + 1}/{max_attempts} - Status: {status} {progress}")
                    
                    if status == "SUCCESS":
                        print(f"\n✅ Image generation complete!")
                        result_data = data["data"]["data"]
                        output = result_data.get("output", [])
                        
                        if output:
                            image_url = output[0] if isinstance(output, list) else output
                            print(f"🖼️  Image URL: {image_url}")
                        
                        logs = result_data.get("logs", "")
                        if "Generation took" in logs:
                            duration_line = [l for l in logs.split("\n") if "Generation took" in l]
                            if duration_line:
                                print(f"⏱️  {duration_line[0]}")
                        
                        return data
                        
                    elif status in ["FAILED"]:
                        print(f"❌ Generation failed: {data}")
                        return None
                        
                    else:
                        time.sleep(poll_interval)
                else:
                    # Fallback to standard Replicate format
                    status = data.get("status")
                    print(f"📊 Attempt {attempt + 1}/{max_attempts} - Status: {status}")
                    
                    if status in ["succeeded", "completed"]:
                        print(f"\n✅ Image generation complete!")
                        output = data.get("output", [])
                        if output:
                            image_url = output[0] if isinstance(output, list) else output
                            print(f"🖼️  Image URL: {image_url}")
                        return data
                    elif status in ["failed", "canceled"]:
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
