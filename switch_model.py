#!/usr/bin/env python3
"""
LM Studio Model Switcher for Cursor
Easily switch between different models by updating Cursor settings
"""

import os
import json
import shutil
import sys
from pathlib import Path

# Available models and their configurations
MODELS = {
    "1": {
        "name": "Qwen3-30B (General AI)",
        "file": "qwen3-30b.json",
        "model": "qwen/qwen3-30b-a3b-2507",
        "description": "30B parameters - Best for complex reasoning and general AI tasks"
    },
    "2": {
        "name": "Qwen2.5-Coder-14B (Coding)",
        "file": "qwen2.5-coder-14b.json", 
        "model": "qwen/qwen2.5-coder-14b",
        "description": "14B parameters - Optimized for coding and programming tasks"
    },
    "3": {
        "name": "DeepSeek-R1-8B (Reasoning)",
        "file": "deepseek-r1-8b.json",
        "model": "deepseek-r1-distill-llama-8b", 
        "description": "8B parameters - Advanced reasoning, math, and logic"
    },
    "4": {
        "name": "Qwen3-Coder-480B (Large Coding)",
        "file": "qwen3-coder-480b.json",
        "model": "qwen/qwen3-coder-480b",
        "description": "480B parameters - Most powerful coding model (requires lots of RAM)"
    },
    "5": {
        "name": "Llama-3.1-8B (Balanced)",
        "file": "llama-3.1-8b.json",
        "model": "meta-llama-3.1-8b-instruct",
        "description": "8B parameters - Good balance of speed and capability"
    },
    "6": {
        "name": "Llama-3.2-3B (Fast)",
        "file": "llama-3.2-3b.json", 
        "model": "llama-3.2-3b-instruct",
        "description": "3B parameters - Fastest responses, lightweight"
    },
    "7": {
        "name": "Mistral-Nemo (Balanced)",
        "file": "mistral-nemo.json",
        "model": "mistral-nemo-instruct-2407",
        "description": "12B parameters - Well-rounded performance"
    },
    "8": {
        "name": "Devstral-Small (Code)",
        "file": "devstral-small.json",
        "model": "devstral-small-2507-mlx",
        "description": "22B parameters - Specialized for code generation"
    },
    "9": {
        "name": "Hermes-3-3B (Creative)",
        "file": "hermes-3-3b.json",
        "model": "hermes-3-llama-3.2-3b",
        "description": "3B parameters - Great for creative writing and chat"
    },
    "10": {
        "name": "Claude2-Alpaca-13B",
        "file": "claude2-alpaca.json",
        "model": "claude2-alpaca-13b", 
        "description": "13B parameters - Good instruction following"
    },
    "11": {
        "name": "GPT-OSS-20B",
        "file": "gpt-oss-20b.json",
        "model": "openai/gpt-oss-20b",
        "description": "20B parameters - GPT-like responses"
    }
}

def get_cursor_settings_path():
    """Get the path to Cursor settings.json"""
    home = Path.home()
    cursor_settings = home / "Library/Application Support/Cursor/User/settings.json"
    
    if cursor_settings.exists():
        return cursor_settings
    else:
        print(f"❌ Cursor settings.json not found at: {cursor_settings}")
        print("   Please make sure Cursor is installed and has been run at least once.")
        return None

def backup_current_settings(settings_path):
    """Create a backup of current settings"""
    backup_path = settings_path.parent / "settings.json.backup"
    shutil.copy2(settings_path, backup_path)
    print(f"📋 Current settings backed up to: settings.json.backup")

def switch_model(model_key):
    """Switch to the specified model"""
    if model_key not in MODELS:
        print(f"❌ Invalid model key: {model_key}")
        return False
    
    model_info = MODELS[model_key]
    config_file = Path(__file__).parent / "cursor_configs" / model_info["file"]
    
    if not config_file.exists():
        print(f"❌ Configuration file not found: {config_file}")
        return False
    
    settings_path = get_cursor_settings_path()
    if not settings_path:
        return False
    
    try:
        # Backup current settings
        backup_current_settings(settings_path)
        
        # Copy new configuration
        shutil.copy2(config_file, settings_path)
        
        print(f"✅ Successfully switched to: {model_info['name']}")
        print(f"🤖 Model: {model_info['model']}")
        print(f"📝 {model_info['description']}")
        print(f"\n🔄 Please restart Cursor for changes to take effect!")
        print(f"💡 Make sure to load '{model_info['model']}' in LM Studio first!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error switching model: {e}")
        return False

def show_current_model():
    """Show currently configured model"""
    settings_path = get_cursor_settings_path()
    if not settings_path:
        return
    
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        current_model = settings.get('openai.model', 'Not configured')
        api_base = settings.get('openai.apiBase', 'Not configured')
        
        print(f"🤖 Current model: {current_model}")
        print(f"🔗 API base: {api_base}")
        
        # Find which model this corresponds to
        for key, info in MODELS.items():
            if info['model'] == current_model:
                print(f"📝 {info['description']}")
                break
                
    except Exception as e:
        print(f"❌ Error reading current settings: {e}")

def main():
    print("🔧 LM Studio Model Switcher for Cursor")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "current":
            show_current_model()
            return
        elif sys.argv[1] in MODELS:
            switch_model(sys.argv[1])
            return
    
    print("📋 Available Models:")
    print()
    
    for key, info in MODELS.items():
        print(f"{key:2}. {info['name']}")
        print(f"    🤖 {info['model']}")
        print(f"    📝 {info['description']}")
        print()
    
    print("Commands:")
    print("  python switch_model.py [1-11]  - Switch to model")
    print("  python switch_model.py current - Show current model")
    print()
    
    try:
        choice = input("Enter model number (1-11) or 'q' to quit: ").strip()
        
        if choice.lower() == 'q':
            print("👋 Goodbye!")
            return
            
        if choice in MODELS:
            switch_model(choice)
        else:
            print("❌ Invalid choice. Please enter a number 1-11.")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
