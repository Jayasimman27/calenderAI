#!/usr/bin/env python3
"""
Startup script for TailorTalk on Railway
Handles common deployment issues and provides better error reporting
"""

import os
import sys
import uvicorn
from app.main import app

def main():
    """Main startup function with error handling"""
    try:
        # Get port from environment variable
        port = int(os.environ.get("PORT", 8004))
        
        # Log startup information
        print(f"🚀 Starting TailorTalk on port {port}")
        print(f"📊 Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'development')}")
        
        # Check for required environment variables
        if not os.environ.get("GOOGLE_SERVICE_ACCOUNT"):
            print("⚠️  Warning: GOOGLE_SERVICE_ACCOUNT not set")
            print("   Calendar features will not work without this")
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 