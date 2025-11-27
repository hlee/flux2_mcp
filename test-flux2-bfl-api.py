#!/usr/bin/env python3
"""
Flux 2 API Test Script - BFL Direct API
Tests FLUX.2 [pro] and [flex] models using the official BFL API
"""

import requests
import time
import json
import sys
import os

# BFL API Key - set via environment variable or config
BFL_API_KEY = os.getenv("BFL_API_KEY", "")

if not BFL_API_KEY:
    print("❌ Error: BFL_API_KEY environment variable not set!")
    print("Please set it with: export BFL_API_KEY='your-bfl-api-key'")
    sys.exit(1)

BASE_URL = "https://api.bfl.ai/v1"


def generate_image_pro(prompt, width=1024, height=1024, seed=None):
    """Generate an image using FLUX.2 [pro]"""
    url = f"{BASE_URL}/flux-2-pro"
    
    headers = {
        "accept": "application/json",
        "x-key": BFL_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "safety_tolerance": 2
    }
    
    if seed is not None:
        payload["seed"] = seed
    
    print(f"🚀 Generating image with FLUX.2 [pro]")
    print(f"📝 Prompt: '{prompt}'")
    print(f"📐 Size: {width}x{height}")
    print(f"📍 URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get("id")
            polling_url = data.get("polling_url")
            cost = data.get("cost")
            output_mp = data.get("output_mp")
            
            print(f"✅ Task created successfully!")
            print(f"🆔 Task ID: {task_id}")
            print(f"💰 Cost: {cost} credits")
            print(f"📦 Output MP: {output_mp}")
            
            return task_id, polling_url
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None, None


def generate_image_flex(prompt, width=1024, height=1024, steps=50, guidance=4.5, seed=None):
    """Generate an image using FLUX.2 [flex]"""
    url = f"{BASE_URL}/flux-2-flex"
    
    headers = {
        "accept": "application/json",
        "x-key": BFL_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "guidance": guidance,
        "safety_tolerance": 2,
        "output_format": "png"
    }
    
    if seed is not None:
        payload["seed"] = seed
    
    print(f"🚀 Generating image with FLUX.2 [flex]")
    print(f"📝 Prompt: '{prompt}'")
    print(f"📐 Size: {width}x{height}")
    print(f"🎚️  Steps: {steps}, Guidance: {guidance}")
    print(f"📍 URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get("id")
            polling_url = data.get("polling_url")
            cost = data.get("cost")
            output_mp = data.get("output_mp")
            
            print(f"✅ Task created successfully!")
            print(f"🆔 Task ID: {task_id}")
            print(f"💰 Cost: {cost} credits")
            print(f"📦 Output MP: {output_mp}")
            
            return task_id, polling_url
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None, None


def get_result(polling_url, task_id, max_attempts=60, poll_interval=2):
    """Poll for image generation result"""
    headers = {
        "accept": "application/json",
        "x-key": BFL_API_KEY
    }
    
    print(f"\n⏳ Polling for results (Task ID: {task_id})")
    print(f"📍 Polling URL: {polling_url}")
    print(f"⏸️  Waiting 3 seconds before first poll...")
    time.sleep(3)
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(polling_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                
                print(f"📊 Attempt {attempt + 1}/{max_attempts} - Status: {status}")
                
                if status == "Ready":
                    print(f"\n✅ Image generation complete!")
                    result = data.get("result", {})
                    
                    # Handle different response formats
                    if "sample" in result:
                        image_url = result.get("sample")
                        print(f"🖼️  Image URL: {image_url}")
                    elif "images" in result:
                        images = result.get("images", [])
                        if images:
                            image_url = images[0].get("url")
                            print(f"🖼️  Image URL: {image_url}")
                    
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
    print("=" * 70)
    print("FLUX.2 API Test - BFL Direct API")
    print("=" * 70)
    
    # Test 1: FLUX.2 [pro] - Fast generation
    print("\n" + "=" * 70)
    print("Test 1: FLUX.2 [pro] - Fast Production Model")
    print("=" * 70)
    
    prompt_pro = "a beautiful sunset over mountains, photorealistic, 85mm lens"
    task_id, polling_url = generate_image_pro(prompt_pro, width=1024, height=768, seed=42)
    
    if task_id and polling_url:
        result = get_result(polling_url, task_id)
        if result:
            print(f"✅ Test 1 passed!")
        else:
            print(f"❌ Test 1 failed - polling error")
    else:
        print(f"❌ Test 1 failed - generation error")
    
    # Test 2: FLUX.2 [flex] - High quality with controls
    print("\n" + "=" * 70)
    print("Test 2: FLUX.2 [flex] - High Quality with Controls")
    print("=" * 70)
    
    prompt_flex = "Clean poster layout with bold typography in #FF5733 and #1E90FF, modern design"
    task_id, polling_url = generate_image_flex(
        prompt_flex, 
        width=1024, 
        height=1024, 
        steps=50, 
        guidance=5.0,
        seed=42
    )
    
    if task_id and polling_url:
        result = get_result(polling_url, task_id)
        if result:
            print(f"✅ Test 2 passed!")
        else:
            print(f"❌ Test 2 failed - polling error")
    else:
        print(f"❌ Test 2 failed - generation error")
    
    print("\n" + "=" * 70)
    print("✅ Testing completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
