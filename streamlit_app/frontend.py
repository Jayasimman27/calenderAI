import streamlit as st
import requests
import json
from datetime import datetime, timezone
import time

# Configure the page
st.set_page_config(
    page_title="TailorTalk",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8004"

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_message(message):
    """Send a message to the API and get response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"content": message, "timestamp": datetime.now(timezone.utc).isoformat()},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["message"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to API: {str(e)}"

def get_calendar_events():
    """Get calendar events from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/calendar/events", timeout=10)
        if response.status_code == 200:
            return response.json()["events"]
        else:
            return []
    except:
        return []

def main():
    # Header
    st.markdown('<h1 class="main-header">🗓️ TailorTalk</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI Calendar Assistant")
    
    # Sidebar
    with st.sidebar:
        st.header("📅 Calendar")
        
        # Check API health
        if check_api_health():
            st.success("✅ API Connected")
            
            # Get calendar events
            if st.button("🔄 Refresh Events"):
                events = get_calendar_events()
                if events:
                    st.subheader("Upcoming Events:")
                    for event in events:
                        with st.expander(f"📅 {event['summary']}"):
                            st.write(f"**Start:** {event['start']}")
                            st.write(f"**End:** {event['end']}")
                            if event.get('description'):
                                st.write(f"**Description:** {event['description']}")
                            if event.get('location'):
                                st.write(f"**Location:** {event['location']}")
                else:
                    st.info("No upcoming events found.")
        else:
            st.error("❌ API Not Connected")
            st.info("Make sure the FastAPI server is running on localhost:8000")
    
    # Main chat interface
    st.markdown("---")
    
    # Initialize chat history and processing flag
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    # Display chat history
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>TailorTalk:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Example prompts
    st.markdown("**💡 Quick Actions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Show my events", key="show_events"):
            if not st.session_state.processing:
                st.session_state.processing = True
                user_message = "Show my upcoming calendar events"
                st.session_state.messages.append({"role": "user", "content": user_message})
                with st.spinner("Getting your events..."):
                    response = send_message(user_message)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.processing = False
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear chat", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
    
    with col3:
        if st.button("🔄 Refresh", key="refresh"):
            st.rerun()
    
    # Example prompts
    st.markdown("**💡 Example prompts you can type:**")
    st.markdown("""
    - `meet at 4PM today for playing cricket`
    - `create a meeting at 3 PM tomorrow for project review`
    - `schedule an event at 6 PM today for dinner with friends`
    - `add meeting at 2 PM today for doctor appointment`
    """)
    
    # Chat input
    st.markdown("---")
    user_input = st.text_input(
        "💬 Ask me anything about your calendar:",
        placeholder="e.g., 'meet at 4PM today for playing cricket', 'Show my events', 'What's on my schedule today?'",
        key="user_input"
    )
    
    # Handle message sending
    send_clicked = st.button("Send", key="send_button")
    enter_pressed = user_input and user_input.strip()
    
    if (send_clicked or enter_pressed) and not st.session_state.processing:
        if user_input and user_input.strip():
            # Set processing flag to prevent duplicate processing
            st.session_state.processing = True
            
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get response from API
            with st.spinner("TailorTalk is thinking..."):
                response = send_message(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Reset processing flag and rerun
            st.session_state.processing = False
           #st.rerun()

if __name__ == "__main__":
    main() 