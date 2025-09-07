#!/usr/bin/env python3
"""
Ultra minimal configuration for LM Studio context issues
Forces extremely short responses and minimal context usage
"""

import json
import shutil
from pathlib import Path

def get_cursor_settings_path():
    """Get the path to Cursor settings.json"""
    home = Path.home()
    return home / "Library/Application Support/Cursor/User/settings.json"

def create_ultra_minimal_config():
    """Create ultra minimal configuration to avoid all context issues"""
    settings_path = get_cursor_settings_path()
    
    if not settings_path.exists():
        print(f"❌ Cursor settings.json not found at: {settings_path}")
        return False
    
    try:
        # Backup current settings
        backup_path = settings_path.parent / "settings.json.backup.ultra_minimal"
        shutil.copy2(settings_path, backup_path)
        print(f"📋 Settings backed up to: settings.json.backup.ultra_minimal")
        
        # Read current settings
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        # Ultra minimal settings - forces very short context
        settings['openai.apiKey'] = 'lm-studio-key'
        settings['openai.apiBase'] = 'http://localhost:8000/v1'
        settings['openai.model'] = 'llama-3.2-3b-instruct'  # Smallest model
        settings['openai.maxTokens'] = 50  # Extremely short responses
        settings['openai.temperature'] = 0.1  # Very focused
        
        # Additional settings to minimize context
        settings['openai.topP'] = 0.9
        settings['openai.frequencyPenalty'] = 0.0
        settings['openai.presencePenalty'] = 0.0
        
        # Write updated settings
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        
        print(f"✅ Ultra minimal configuration applied!")
        print(f"🤖 Model: llama-3.2-3b-instruct (3B - smallest)")
        print(f"🔢 Max tokens: 50 (extremely short)")
        print(f"🌡️  Temperature: 0.1 (very focused)")
        print(f"\n📋 NEXT STEPS:")
        print(f"1. Load 'llama-3.2-3b-instruct' in LM Studio")
        print(f"2. Restart Cursor")
        print(f"3. Start a NEW chat (don't continue old conversations)")
        print(f"4. Test with very short questions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating ultra minimal config: {e}")
        return False

def check_current_config():
    """Check current Cursor configuration"""
    settings_path = get_cursor_settings_path()
    
    if not settings_path.exists():
        print(f"❌ Cursor settings.json not found")
        return
    
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        print("🔍 Current Cursor Configuration:")
        print(f"   Model: {settings.get('openai.model', 'Not set')}")
        print(f"   Max Tokens: {settings.get('openai.maxTokens', 'Not set')}")
        print(f"   Temperature: {settings.get('openai.temperature', 'Not set')}")
        print(f"   API Base: {settings.get('openai.apiBase', 'Not set')}")
        
    except Exception as e:
        print(f"❌ Error reading config: {e}")

def main():
    print("🚨 Ultra Minimal LM Studio Configuration")
    print("=" * 50)
    print("This creates the most conservative settings possible.")
    print("Use this when even 4000 tokens context isn't enough.")
    print()
    
    check_current_config()
    print()
    
    print("💡 This will:")
    print("   - Switch to smallest model (llama-3.2-3b-instruct)")
    print("   - Limit responses to 50 tokens maximum")
    print("   - Use very low temperature for consistency")
    print("   - Minimize all context usage")
    print()
    
    choice = input("Apply ultra minimal config? (y/n): ").strip().lower()
    
    if choice == 'y':
        create_ultra_minimal_config()
    else:
        print("👍 Configuration not changed.")
        print()
        print("🔧 Alternative solutions:")
        print("1. Try increasing LM Studio context to 8192 or 16384")
        print("2. Use a different model with better context handling")
        print("3. Always start fresh conversations in Cursor")

if __name__ == "__main__":
    main()
