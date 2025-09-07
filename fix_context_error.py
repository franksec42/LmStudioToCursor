#!/usr/bin/env python3
"""
Quick fix for LM Studio context length errors
Updates Cursor settings with safe token limits
"""

import json
import shutil
from pathlib import Path

def get_cursor_settings_path():
    """Get the path to Cursor settings.json"""
    home = Path.home()
    return home / "Library/Application Support/Cursor/User/settings.json"

def fix_context_error():
    """Fix the context length error by reducing maxTokens"""
    settings_path = get_cursor_settings_path()
    
    if not settings_path.exists():
        print(f"❌ Cursor settings.json not found at: {settings_path}")
        return False
    
    try:
        # Backup current settings
        backup_path = settings_path.parent / "settings.json.backup.context_fix"
        shutil.copy2(settings_path, backup_path)
        print(f"📋 Settings backed up to: settings.json.backup.context_fix")
        
        # Read current settings
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        # Update with safe token limits
        current_model = settings.get('openai.model', 'unknown')
        
        # Set safe token limits based on model
        if 'coder' in current_model or '3b' in current_model:
            safe_tokens = 256  # Very conservative for coding/small models
        elif '8b' in current_model:
            safe_tokens = 384  # Small for 8B models
        else:
            safe_tokens = 512  # Default safe limit
        
        settings['openai.maxTokens'] = safe_tokens
        settings['openai.temperature'] = settings.get('openai.temperature', 0.7)
        
        # Write updated settings
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        
        print(f"✅ Context error fixed!")
        print(f"🤖 Model: {current_model}")
        print(f"🔢 Max tokens reduced to: {safe_tokens}")
        print(f"🌡️  Temperature: {settings['openai.temperature']}")
        print(f"\n🔄 Please restart Cursor for changes to take effect!")
        print(f"💡 This will give shorter but working responses.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing context error: {e}")
        return False

def main():
    print("🔧 LM Studio Context Error Fix")
    print("=" * 40)
    print("This will reduce maxTokens to prevent context overflow errors.")
    print()
    
    fix_context_error()

if __name__ == "__main__":
    main()
