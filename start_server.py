#!/usr/bin/env python3
"""
LM Studio Connector Startup Script
Automatically starts the FastAPI server with proper configuration
"""

import json
import sys
import subprocess
import os
import argparse
import requests
import time
from pathlib import Path

def load_config(config_path="config.json"):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file {config_path} not found. Using defaults.")
        return {
            "lm_studio": {"url": "http://localhost:1234", "timeout": 300},
            "server": {"host": "0.0.0.0", "port": 8000, "reload": True}
        }
    except json.JSONDecodeError as e:
        print(f"Error parsing config file: {e}")
        sys.exit(1)

def check_lm_studio_connection(url):
    """Check if LM Studio is running and accessible"""
    try:
        response = requests.get(f"{url}/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_count = len(models.get('data', []))
            print(f"✅ LM Studio is running at {url}")
            print(f"📋 Found {model_count} available models")
            return True
        else:
            print(f"⚠️  LM Studio responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to LM Studio at {url}")
        print(f"   Error: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['fastapi', 'uvicorn', 'httpx', 'pydantic']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True

def start_server(config):
    """Start the FastAPI server with uvicorn"""
    server_config = config.get('server', {})
    host = server_config.get('host', '0.0.0.0')
    port = server_config.get('port', 8000)
    reload = server_config.get('reload', True)
    
    print(f"🚀 Starting LM Studio Connector on {host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"🔗 OpenAI-compatible endpoint: http://{host}:{port}/v1/chat/completions")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "llm_server:app",
        "--host", host,
        "--port", str(port)
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Start LM Studio Connector")
    parser.add_argument("--config", "-c", default="config.json", 
                       help="Configuration file path (default: config.json)")
    parser.add_argument("--skip-checks", action="store_true",
                       help="Skip dependency and LM Studio connection checks")
    parser.add_argument("--port", "-p", type=int,
                       help="Override server port")
    parser.add_argument("--host", default=None,
                       help="Override server host")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.port:
        config.setdefault('server', {})['port'] = args.port
    if args.host:
        config.setdefault('server', {})['host'] = args.host
    
    print("🔧 LM Studio Connector v2.0.0")
    print("=" * 50)
    
    if not args.skip_checks:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Check LM Studio connection
        lm_studio_url = config.get('lm_studio', {}).get('url', 'http://localhost:1234')
        if not check_lm_studio_connection(lm_studio_url):
            print("\n⚠️  LM Studio is not accessible. Make sure:")
            print("   1. LM Studio is running")
            print("   2. Local Server is started in LM Studio")
            print("   3. The correct URL is configured")
            print(f"   4. Current URL: {lm_studio_url}")
            print("\n🔄 You can still start the connector, but it won't work until LM Studio is running.")
            
            response = input("\nDo you want to continue anyway? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                sys.exit(1)
    
    print()
    
    # Start the server
    start_server(config)

if __name__ == "__main__":
    main()
