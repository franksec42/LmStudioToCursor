#!/usr/bin/env python3
"""
Debug script to see what Cursor is actually sending to LM Studio
Logs the requests to understand context usage
"""

import json
import time
from pathlib import Path

def monitor_connector_logs():
    """Monitor what's being sent through the connector"""
    print("🔍 Request Monitoring Guide")
    print("=" * 40)
    print()
    print("To see what Cursor is actually sending:")
    print()
    print("1. 📋 Check connector terminal output:")
    print("   Look at your uvicorn terminal for HTTP requests")
    print("   You should see lines like:")
    print("   INFO:     127.0.0.1:xxxxx - \"POST /v1/chat/completions HTTP/1.1\" 200 OK")
    print()
    print("2. 🔧 Enable detailed logging:")
    print("   Add --log-level debug to uvicorn command:")
    print("   uvicorn llm_server:app --reload --host 0.0.0.0 --port 8000 --log-level debug")
    print()
    print("3. 📊 Check message lengths:")
    print("   The issue might be very long messages from Cursor")
    print("   Even 'short' conversations can have long system prompts")
    print()
    print("4. 🧪 Test with minimal settings:")
    print("   python3 ultra_minimal_config.py")
    print("   This forces 50-token responses and uses smallest model")

def check_model_context_in_lm_studio():
    """Instructions to verify actual context in LM Studio"""
    print("\n🔧 Verify LM Studio Context Settings:")
    print("=" * 45)
    print()
    print("1. 📋 In LM Studio interface:")
    print("   - Look at the loaded model")
    print("   - Click the gear/settings icon next to model name")
    print("   - Check 'Context Length' or 'Max Context' value")
    print("   - Verify it shows 4000 (not 2048 or other value)")
    print()
    print("2. 🔄 If context is not 4000:")
    print("   - Change it to 4000, 8192, or 16384")
    print("   - Click 'Apply' or 'Save'")
    print("   - IMPORTANT: Reload/restart the model")
    print()
    print("3. 📊 Model-specific context limits:")
    print("   - Some models have hard limits regardless of settings")
    print("   - qwen/qwen3-30b-a3b-2507 might have built-in limits")
    print("   - Try switching to llama-3.2-3b-instruct for testing")

def create_emergency_config():
    """Create emergency working configuration"""
    print("\n🚨 Emergency Configuration")
    print("=" * 30)
    print()
    print("If nothing else works, try this manual configuration:")
    print()
    print("In your Cursor settings.json, use EXACTLY this:")
    print()
    config = {
        "openai.apiKey": "lm-studio-key",
        "openai.apiBase": "http://localhost:8000/v1", 
        "openai.model": "llama-3.2-3b-instruct",
        "openai.maxTokens": 30,
        "openai.temperature": 0.1
    }
    print(json.dumps(config, indent=2))
    print()
    print("Then:")
    print("1. Load 'llama-3.2-3b-instruct' in LM Studio")
    print("2. Set context to 2048 (default is fine)")
    print("3. Restart Cursor")
    print("4. Start a completely NEW chat")
    print("5. Ask very short questions")

def main():
    print("🐛 LM Studio Context Debug Helper")
    print("=" * 40)
    print("Even with 4000 tokens, you're getting context errors.")
    print("Let's debug what's actually happening.")
    print()
    
    monitor_connector_logs()
    check_model_context_in_lm_studio()
    create_emergency_config()
    
    print("\n💡 Most Likely Solutions:")
    print("1. 🔄 Switch to llama-3.2-3b-instruct (smallest model)")
    print("2. 📊 Use maxTokens: 30-50 (very short responses)")
    print("3. 🆕 Always start NEW chats (don't continue old ones)")
    print("4. ⬆️  Increase LM Studio context to 8192+")
    
    print(f"\n🚀 Quick fix command:")
    print(f"python3 ultra_minimal_config.py")

if __name__ == "__main__":
    main()
