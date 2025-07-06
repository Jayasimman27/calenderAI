# 🚀 TailorTalk Deployment Guide

This guide will help you deploy TailorTalk to various cloud platforms.

## 📋 Prerequisites

1. **Google Calendar API Setup**
   - Create a Google Cloud Project
   - Enable Google Calendar API
   - Create a Service Account
   - Download the service account JSON file
   - Share your calendar with the service account email

2. **Ollama Setup** (for local AI)
   - Install Ollama on your server
   - Pull TinyLlama model: `ollama pull tinyllama`

## 🌐 Deployment Options

### Option 1: Railway (Recommended)

**Pros**: Easy deployment, good free tier, automatic HTTPS

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Deploy**:
   ```bash
   railway init
   railway up
   ```

4. **Set Environment Variables**:
   - Go to Railway Dashboard
   - Add your `service_account.json` content as `GOOGLE_SERVICE_ACCOUNT`
   - Set `OLLAMA_URL` if using remote Ollama

### Option 2: Render

**Pros**: Free tier available, easy setup

1. **Connect GitHub**:
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository

2. **Create Web Service**:
   - Choose "Web Service"
   - Select your repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**:
   - Add `GOOGLE_SERVICE_ACCOUNT` with your service account JSON
   - Set `OLLAMA_URL` if needed

### Option 3: Fly.io

**Pros**: Global edge deployment, generous free tier

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**:
   ```bash
   fly auth login
   ```

3. **Deploy**:
   ```bash
   fly launch
   fly deploy
   ```

4. **Set Secrets**:
   ```bash
   fly secrets set GOOGLE_SERVICE_ACCOUNT="$(cat service_account.json)"
   ```

## 🔧 Environment Variables

Set these in your cloud platform:

```bash
# Google Calendar (Required)
GOOGLE_SERVICE_ACCOUNT={"type":"service_account",...}

# Ollama (Optional - for remote Ollama)
OLLAMA_URL=http://your-ollama-server:11434

# Port (Auto-set by platform)
PORT=8004
```

## 📝 Service Account Setup

1. **Create Service Account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing
   - Enable Google Calendar API
   - Create Service Account
   - Download JSON key

2. **Share Calendar**:
   - Go to [Google Calendar](https://calendar.google.com)
   - Share your calendar with: `your-service-account@project.iam.gserviceaccount.com`
   - Give "Make changes to events" permission

## 🐳 Docker Deployment

If you prefer Docker:

```bash
# Build image
docker build -t tailortalk .

# Run locally
docker run -p 8004:8004 -e GOOGLE_SERVICE_ACCOUNT="$(cat service_account.json)" tailortalk

# Push to registry
docker tag tailortalk your-registry/tailortalk
docker push your-registry/tailortalk
```

## 🔍 Health Check

Your deployed app will have a health check endpoint:
- `https://your-app.railway.app/health`
- `https://your-app.onrender.com/health`
- `https://your-app.fly.dev/health`

## 🚨 Important Notes

1. **Service Account**: Never commit your `service_account.json` to Git
2. **Ollama**: For production, consider using a hosted Ollama service
3. **CORS**: Update CORS settings for your frontend domain
4. **HTTPS**: All platforms provide automatic HTTPS

## 🆘 Troubleshooting

### Common Issues:

1. **Calendar Permission Error**:
   - Ensure service account has calendar access
   - Check calendar sharing settings

2. **Ollama Connection Error**:
   - Verify Ollama is running
   - Check OLLAMA_URL environment variable

3. **Port Issues**:
   - Use `$PORT` environment variable
   - Don't hardcode port numbers

### Logs:
- Railway: `railway logs`
- Render: Dashboard → Logs
- Fly.io: `fly logs`

## 🎯 Next Steps

After deployment:

1. **Test the API**: `curl https://your-app.railway.app/health`
2. **Update Frontend**: Point your Streamlit app to the new API URL
3. **Monitor**: Check logs for any errors
4. **Scale**: Upgrade plan if needed

## 📞 Support

- Railway: [Discord](https://discord.gg/railway)
- Render: [Documentation](https://render.com/docs)
- Fly.io: [Community](https://community.fly.io) 