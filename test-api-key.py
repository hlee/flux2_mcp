#!/usr/bin/env python3
"""
API Key Diagnostic Script
Tests different authentication formats and endpoints
"""

import requests

API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key

# Test different authentication formats
auth_formats = [
    ("Direct key", API_KEY),
    ("Bearer prefix", f"Bearer {API_KEY}"),
]

# Test different endpoints
endpoints = [
    ("Gemini 2.5 Flash", "https://api.cometapi.com/v1beta/models/gemini-2.5-flash-image:generateContent"),
    ("Gemini 3 Pro", "https://api.cometapi.com/v1beta/models/gemini-3-pro-image:generateContent"),
]

payload = {
    "contents": [{
        "parts": [{
            "text": "test"
        }]
    }]
}

print("=" * 70)
print("API Key Diagnostic Test")
print("=" * 70)

for auth_name, auth_value in auth_formats:
    print(f"\n🔑 Testing with: {auth_name}")
    print("-" * 70)
    
    for endpoint_name, url in endpoints:
        headers = {
            "Authorization": auth_value,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            status = response.status_code
            
            if status == 401:
                result = "❌ 401 Unauthorized (Invalid key)"
            elif status == 403:
                result = "❌ 403 Forbidden (No access)"
            elif status == 404:
                result = "❌ 404 Not Found (Wrong endpoint)"
            elif status == 200:
                result = "✅ 200 OK (Success!)"
            else:
                result = f"⚠️  {status} - {response.text[:100]}"
            
            print(f"  {endpoint_name:20} → {result}")
            
        except Exception as e:
            print(f"  {endpoint_name:20} → ❌ Error: {e}")

print("\n" + "=" * 70)
print("Diagnostic complete")
print("=" * 70)
print("\n💡 Suggestions:")
print("  1. Verify your API key is correct and complete")
print("  2. Check if the key is activated in your CometAPI dashboard")
print("  3. Ensure you have access to Gemini image models")
print("  4. Try generating a new API key if needed")
