#!/usr/bin/env python3
"""
Test script for LM Studio Connector
Verifies that the API server is working correctly
"""

import requests
import json
import time
import sys
from typing import Dict, Any

def test_health_check(base_url: str) -> bool:
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            if data.get('lm_studio_connected'):
                print("✅ LM Studio connection verified")
            else:
                print("⚠️  LM Studio not connected")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_models_endpoint(base_url: str) -> bool:
    """Test the models listing endpoint"""
    try:
        response = requests.get(f"{base_url}/v1/models", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])
            print(f"✅ Models endpoint working: Found {len(models)} models")
            for model in models[:3]:  # Show first 3 models
                print(f"   - {model['id']}")
            return True
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")
        return False

def test_chat_completion(base_url: str, model: str = "lm-studio-model") -> bool:
    """Test the chat completion endpoint"""
    try:
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Hello! Please respond with just 'Test successful' if you can read this."}
            ],
            "temperature": 0.1,
            "max_tokens": 50,
            "stream": False
        }
        
        print("🔄 Testing chat completion (this may take a moment)...")
        response = requests.post(
            f"{base_url}/v1/chat/completions", 
            json=payload, 
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0]['message']['content']
                print(f"✅ Chat completion successful!")
                print(f"   Response: {content[:100]}...")
                return True
            else:
                print("❌ Chat completion: No response content")
                return False
        else:
            print(f"❌ Chat completion failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Chat completion error: {e}")
        return False

def test_streaming_completion(base_url: str, model: str = "lm-studio-model") -> bool:
    """Test streaming chat completion"""
    try:
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Count from 1 to 5, one number per line."}
            ],
            "temperature": 0.1,
            "max_tokens": 50,
            "stream": True
        }
        
        print("🔄 Testing streaming completion...")
        response = requests.post(
            f"{base_url}/v1/chat/completions", 
            json=payload, 
            timeout=30,
            headers={"Content-Type": "application/json"},
            stream=True
        )
        
        if response.status_code == 200:
            chunks_received = 0
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove 'data: ' prefix
                        if data_str.strip() == '[DONE]':
                            break
                        try:
                            chunk_data = json.loads(data_str)
                            if 'choices' in chunk_data:
                                chunks_received += 1
                        except json.JSONDecodeError:
                            continue
            
            if chunks_received > 0:
                print(f"✅ Streaming completion successful! Received {chunks_received} chunks")
                return True
            else:
                print("❌ Streaming completion: No chunks received")
                return False
        else:
            print(f"❌ Streaming completion failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Streaming completion error: {e}")
        return False

def test_config_endpoint(base_url: str) -> bool:
    """Test the configuration endpoint"""
    try:
        response = requests.get(f"{base_url}/config", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Config endpoint working")
            print(f"   LM Studio URL: {data.get('lm_studio_url')}")
            return True
        else:
            print(f"❌ Config endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Config endpoint error: {e}")
        return False

def run_all_tests(base_url: str = "http://localhost:8000") -> bool:
    """Run all tests"""
    print("🧪 LM Studio Connector Test Suite")
    print("=" * 50)
    print(f"Testing server at: {base_url}")
    print()
    
    tests = [
        ("Health Check", lambda: test_health_check(base_url)),
        ("Configuration", lambda: test_config_endpoint(base_url)),
        ("Models Endpoint", lambda: test_models_endpoint(base_url)),
        ("Chat Completion", lambda: test_chat_completion(base_url)),
        ("Streaming Completion", lambda: test_streaming_completion(base_url)),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🧪 Running {test_name}...")
        try:
            if test_func():
                passed += 1
            print()
        except KeyboardInterrupt:
            print("\n⏹️  Tests interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error in {test_name}: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your LM Studio Connector is working perfectly.")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test LM Studio Connector")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="Base URL of the connector server")
    parser.add_argument("--quick", action="store_true",
                       help="Run only basic tests (skip chat completion)")
    
    args = parser.parse_args()
    
    if args.quick:
        print("🏃 Running quick tests only...")
        success = (
            test_health_check(args.url) and
            test_config_endpoint(args.url) and
            test_models_endpoint(args.url)
        )
    else:
        success = run_all_tests(args.url)
    
    sys.exit(0 if success else 1)
