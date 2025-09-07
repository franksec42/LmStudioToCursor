#!/usr/bin/env python3
"""
Fix LM Studio context length issues
Provides solutions for conversation history overflow
"""

import json
import shutil
from pathlib import Path

def get_cursor_settings_path():
    """Get the path to Cursor settings.json"""
    home = Path.home()
    return home / "Library/Application Support/Cursor/User/settings.json"

def create_minimal_context_config():
    """Create a configuration that minimizes context usage"""
    settings_path = get_cursor_settings_path()
    
    if not settings_path.exists():
        print(f"❌ Cursor settings.json not found at: {settings_path}")
        return False
    
    try:
        # Backup current settings
        backup_path = settings_path.parent / "settings.json.backup.minimal_context"
        shutil.copy2(settings_path, backup_path)
        print(f"📋 Settings backed up to: settings.json.backup.minimal_context")
        
        # Read current settings
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        # Use the smallest, fastest model with minimal context
        settings['openai.model'] = 'llama-3.2-3b-instruct'  # Smallest model
        settings['openai.maxTokens'] = 128  # Very small responses
        settings['openai.temperature'] = 0.3  # More focused responses
        
        # Write updated settings
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        
        print(f"✅ Minimal context configuration applied!")
        print(f"🤖 Switched to: llama-3.2-3b-instruct (smallest model)")
        print(f"🔢 Max tokens: 128 (very short responses)")
        print(f"🌡️  Temperature: 0.3 (focused)")
        print(f"\n🔄 Please restart Cursor and load 'llama-3.2-3b-instruct' in LM Studio!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating minimal config: {e}")
        return False

def show_lm_studio_instructions():
    """Show instructions for fixing LM Studio context"""
    print("\n📋 LM Studio Context Fix Instructions:")
    print("=" * 50)
    print("1. 🔧 INCREASE CONTEXT LENGTH (Recommended):")
    print("   - Open LM Studio")
    print("   - Click the gear icon next to your loaded model")
    print("   - Find 'Context Length' or 'Max Context'")
    print("   - Change from default (usually 2048) to 4096 or 8192")
    print("   - Click 'Reload Model' or restart the model")
    print("   - This allows longer conversations")
    print()
    print("2. 🔄 OR SWITCH TO SMALLER MODEL:")
    print("   - Load 'llama-3.2-3b-instruct' in LM Studio")
    print("   - This model needs much less context")
    print("   - Faster but less capable")
    print()
    print("3. 🗑️  OR CLEAR CONVERSATION:")
    print("   - In Cursor, start a new chat (don't continue old one)")
    print("   - Each new chat starts fresh")
    print()
    print("4. ⚡ CURRENT MODEL CONTEXT USAGE:")
    print("   - qwen/qwen3-30b-a3b-2507: HIGH context usage")
    print("   - llama-3.2-3b-instruct: LOW context usage")
    print("   - deepseek-r1-distill-llama-8b: MEDIUM context usage")

def main():
    print("🔧 LM Studio Context Length Fix")
    print("=" * 40)
    print("Problem: Conversation history exceeds model context window")
    print()
    
    show_lm_studio_instructions()
    print()
    
    choice = input("Apply minimal context config? (y/n): ").strip().lower()
    
    if choice == 'y':
        create_minimal_context_config()
    else:
        print("👍 Follow the LM Studio instructions above to increase context length.")

if __name__ == "__main__":
    main()
