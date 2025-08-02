#!/usr/bin/env python3
"""
Real-time ZTA-ATDS Startup Script
"""

import uvicorn
import asyncio
import sys
import os

def main():
    """Start the real-time ZTA-ATDS application"""
    
    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    print("🚀 Starting ZTA-ATDS Real-Time Application...")
    print("=" * 50)
    print("📊 Real-time threat detection system")
    print("🔗 WebSocket support enabled")
    print("📈 Live dashboard available")
    print("🚨 Real-time alerting system active")
    print("=" * 50)
    
    # Configuration for real-time application
    config = {
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
        "log_level": "info",
        "access_log": True
    }
    
    print(f"🌐 Server will be available at: http://localhost:{config['port']}")
    print(f"📊 Dashboard: http://localhost:{config['port']}/")
    print(f"🔌 WebSocket: ws://localhost:{config['port']}/ws")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            **config
        )
    except KeyboardInterrupt:
        print("\n🛑 Shutting down real-time application...")
        print("✅ Application stopped successfully")

if __name__ == "__main__":
    main() 