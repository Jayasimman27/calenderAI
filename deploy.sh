#!/bin/bash

# TailorTalk Deployment Script
echo "🚀 Deploying TailorTalk..."

# Check if service_account.json exists
if [ ! -f "service_account.json" ]; then
    echo "❌ Error: service_account.json not found!"
    echo "Please create a Google Cloud Service Account and download the JSON file."
    exit 1
fi

# Check if Ollama is running (for local deployment)
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Warning: Ollama is not running on localhost:11434"
    echo "For cloud deployment, set OLLAMA_URL environment variable"
fi

echo "✅ Prerequisites check passed!"

# Choose deployment platform
echo ""
echo "Choose your deployment platform:"
echo "1) Railway (Recommended)"
echo "2) Render"
echo "3) Fly.io"
echo "4) Docker"
echo "5) Local only"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🚂 Deploying to Railway..."
        if ! command -v railway &> /dev/null; then
            echo "Installing Railway CLI..."
            npm install -g @railway/cli
        fi
        railway login
        railway init
        railway up
        ;;
    2)
        echo "🎨 Deploying to Render..."
        echo "1. Go to https://render.com"
        echo "2. Connect your GitHub repository"
        echo "3. Create a new Web Service"
        echo "4. Set environment variables:"
        echo "   - GOOGLE_SERVICE_ACCOUNT: $(cat service_account.json)"
        echo "   - PORT: 8004"
        ;;
    3)
        echo "🛩️  Deploying to Fly.io..."
        if ! command -v fly &> /dev/null; then
            echo "Installing Fly CLI..."
            curl -L https://fly.io/install.sh | sh
        fi
        fly auth login
        fly launch
        fly secrets set GOOGLE_SERVICE_ACCOUNT="$(cat service_account.json)"
        fly deploy
        ;;
    4)
        echo "🐳 Building Docker image..."
        docker build -t tailortalk .
        echo "✅ Docker image built successfully!"
        echo "Run with: docker run -p 8004:8004 -e GOOGLE_SERVICE_ACCOUNT=\"$(cat service_account.json)\" tailortalk"
        ;;
    5)
        echo "🏠 Running locally..."
        echo "Make sure Ollama is running: ollama serve"
        echo "Then run: uvicorn app.main:app --reload --port 8004"
        ;;
    *)
        echo "❌ Invalid choice!"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment completed!"
echo "Check the deployment guide in DEPLOYMENT.md for more details." 