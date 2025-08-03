from langchain.agents import initialize_agent
from langchain.tools import Tool
from app.calendar_utils import GoogleCalendarManager
import dateparser

calendar_manager = GoogleCalendarManager()

def show_events_tool_fn(access_token: str = ""):
    events = calendar_manager.get_upcoming_events(access_token=access_token)
    if not events:
        return "No upcoming events found."
    return "\n".join([
        f"{e['summary']} on {e['start']}" for e in events
    ])

def create_event_tool_fn(summary: str, start_time: str, end_time: str, access_token: str = ""):
    # Parse natural language dates
    parsed_start = dateparser.parse(start_time)
    parsed_end = dateparser.parse(end_time)
    if not parsed_start or not parsed_end:
        return f"Could not parse start or end time. Please provide a valid date/time."
    # Convert to ISO format
    start_iso = parsed_start.isoformat()
    end_iso = parsed_end.isoformat()
    event = calendar_manager.create_event(summary, start_iso, end_iso, access_token=access_token)
    return f"Created event '{event['summary']}' on {event['start']}"

def delete_event_tool_fn(summary: str, access_token: str = ""):
    event = calendar_manager.find_event_by_title(summary, access_token=access_token)
    if not event:
        return f"Event '{summary}' not found."
    calendar_manager.delete_event(event['id'], access_token=access_token)
    return f"Deleted event '{summary}'"

def edit_event_tool_fn(summary: str, new_end_time: str, access_token: str = ""):
    event = calendar_manager.find_event_by_title(summary, access_token=access_token)
    if not event:
        return f"Event '{summary}' not found."
    parsed_end = dateparser.parse(new_end_time)
    if not parsed_end:
        return f"Could not parse new end time. Please provide a valid date/time."
    new_end_iso = parsed_end.isoformat()
    updated = calendar_manager.update_event(event['id'], end_time=new_end_iso, access_token=access_token)
    return f"Updated event '{updated['summary']}' to end at {updated['end']}"

show_events_tool = Tool(
    name="ShowCalendarEvents",
    func=show_events_tool_fn,
    description="Show upcoming Google Calendar events."
)

create_event_tool = Tool(
    name="CreateCalendarEvent",
    func=create_event_tool_fn,
    description="Create a Google Calendar event. Args: summary, start_time (ISO), end_time (ISO), access_token."
)

delete_event_tool = Tool(
    name="DeleteCalendarEvent",
    func=delete_event_tool_fn,
    description="Delete a Google Calendar event by summary/title. Args: summary, access_token."
)

edit_event_tool = Tool(
    name="EditCalendarEvent",
    func=edit_event_tool_fn,
    description="Edit a Google Calendar event's end time. Args: summary, new_end_time (ISO), access_token."
)

tools = [show_events_tool, create_event_tool, delete_event_tool, edit_event_tool] 