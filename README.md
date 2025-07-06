# 🗓️ TailorTalk

An intelligent AI assistant that helps you manage your Google Calendar through natural language conversations. Built with FastAPI, LangChain, and Streamlit.

## 🚀 Features

- **Natural Language Calendar Management**: Ask TailorTalk to create, update, or delete calendar events using plain English
- **Smart Event Scheduling**: Automatically parse dates, times, and event details from your requests
- **Real-time Calendar Integration**: Direct integration with Google Calendar API
- **Beautiful Chat Interface**: Modern Streamlit-based UI for seamless interaction
- **RESTful API**: FastAPI backend for easy integration with other applications

## 📁 Project Structure

```
tailortalk/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry
│   ├── calendar_utils.py        # Google Calendar logic
│   ├── agent.py                 # LangChain/LangGraph agent logic
│   └── models.py                # Pydantic models
├── streamlit_app/
│   └── frontend.py              # Streamlit chat UI
├── service_account.json         # Service account key
├── requirements.txt             # All dependencies
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- OpenAI API key

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd tailortalk
pip install -r requirements.txt
```

### 2. Google Calendar API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create a Service Account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name (e.g., "tailortalk-calendar")
   - Grant "Calendar API Admin" role
5. Create and download a JSON key:
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key" > "JSON"
   - Download the JSON file
6. Replace the placeholder `service_account.json` with your downloaded file

### 3. Environment Variables

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Calendar Sharing

Share your Google Calendar with the service account email address (found in the JSON file) with "Make changes to events" permissions.

## 🚀 Running the Application

### Option 1: Run Both Backend and Frontend

1. **Start the FastAPI backend:**
   ```bash
   cd app
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Streamlit frontend (in a new terminal):**
   ```bash
   streamlit run streamlit_app/frontend.py
   ```

3. Open your browser and go to `http://localhost:8501`

### Option 2: API Only

If you only want to use the API:

```bash
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📖 Usage Examples

### Chat Interface

Once the application is running, you can interact with TailorTalk using natural language:

- **"Show my upcoming events"** - Display all calendar events for the next 7 days
- **"Create a meeting tomorrow at 2 PM for 1 hour called 'Team Standup'"** - Create a new event
- **"What's on my schedule today?"** - Show today's events
- **"Delete the meeting with ID abc123"** - Remove a specific event
- **"Update my meeting to start at 3 PM instead"** - Modify existing events

### API Endpoints

#### Chat Endpoint
```bash
POST /chat
{
  "content": "Show my upcoming events",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Calendar Events
```bash
GET /calendar/events
```

#### Health Check
```bash
GET /health
```

## 🔧 Configuration

### Customizing the Agent

You can modify the agent behavior by editing `app/agent.py`:

- Change the LLM model in the `TailorTalkAgent.__init__()` method
- Add new tools to the `tools` list
- Modify the prompt template for different responses

### Calendar Settings

Adjust calendar behavior in `app/calendar_utils.py`:

- Change the default time range for fetching events
- Modify timezone settings
- Add custom event formatting

## 🐛 Troubleshooting

### Common Issues

1. **"API Not Connected" error in Streamlit**
   - Make sure the FastAPI server is running on port 8000
   - Check that the API_BASE_URL in `frontend.py` matches your server

2. **Google Calendar authentication errors**
   - Verify your `service_account.json` is correctly formatted
   - Ensure the service account has the necessary permissions
   - Check that you've shared your calendar with the service account email

3. **OpenAI API errors**
   - Verify your `OPENAI_API_KEY` is set correctly
   - Check your OpenAI account has sufficient credits

4. **Import errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
#Deployment 
I tried to deploy in railway and render but due to time constraints i couldn't 
## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [LangChain](https://langchain.com/) for AI agent capabilities
- [Streamlit](https://streamlit.io/) for the beautiful UI
- [Google Calendar API](https://developers.google.com/calendar) for calendar integration 
