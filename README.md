# 🗓️ calenderAI

An intelligent AI assistant that helps you manage your Google Calendar through natural language conversations. Built with FastAPI (backend) and React + Vite (frontend).

## 🚀 Features

- **Natural Language Calendar Management**: Ask TailorTalk to create, update, or delete calendar events using plain English
- **Smart Event Scheduling**: Automatically parse dates, times, and event details from your requests
- **Real-time Google Calendar Integration**: Direct integration with Google Calendar API using OAuth2
- **Modern Chat UI**: Beautiful React-based interface with Google login and interactive chat bot
- **RESTful API**: FastAPI backend for easy integration with other applications

## 📁 Project Structure

```
tailortalk/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry
│   ├── calendar_utils.py        # Google Calendar logic
│   ├── agent.py                 # AI agent logic
│   └── models.py                # Pydantic models
├── frontend/
│   ├── src/                     # React app source code
│   └── ...
├── requirements.txt             # Backend dependencies
├── service_account.json         # (Legacy, not used for OAuth2 user flow)
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 18+
- Google Cloud Platform account

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd tailortalk
cd frontend
npm install
```

### 2. Google OAuth Setup (For Real User Calendar Access)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Go to **APIs & Services > Credentials**
5. Click **Create Credentials > OAuth client ID**
   - Application type: Web application
   - Authorized JavaScript origins: `http://localhost:5173`
   - Authorized redirect URIs: `http://localhost:5173`
6. Download your OAuth client credentials (Client ID)
7. Go to **APIs & Services > OAuth consent screen**
   - Fill in app info (name, support email, etc.)
   - Add your Google account as a **Test user**
   - Save

### 3. Environment Variables

Create a `.env` file in the root directory for backend secrets (if needed):
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Configure the Frontend

- In `frontend/src/main.jsx`, use your Google OAuth **Client ID** in the `GoogleOAuthProvider`.

## 🚀 Running the Application

### 1. Start the FastAPI Backend
```bash
cd app
uvicorn main:app --reload --port 8004
```

### 2. Start the React Frontend
```bash
cd frontend
npm run dev
```

## 📖 Usage

- **Login with Google** (must be a test user if app is not verified)
- Use the chat bot to:
  - "Show my upcoming events"
  - "Create an event on July 25 at 6pm for dinner with friends"
  - "Edit the event 'dinner with friends' on July 25 to end at 8pm"
  - "Delete the event 'dinner with friends' on July 25"
- All actions are performed on your real Google Calendar!


