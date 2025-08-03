import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

class GoogleCalendarManager:
    def __init__(self, service_account_file: str = "service_account.json"):
        """
        Initialize Google Calendar manager with service account credentials
        """
        self.service_account_file = service_account_file
        self.service: Optional[Any] = None
        self._authenticate()
    
    def _authenticate(self):
        """
        Authenticate with Google Calendar API using service account
        """
        try:
            # Check if service account is provided via environment variable
            service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT')
            
            if service_account_json:
                # Use environment variable
                import json
                service_account_info = json.loads(service_account_json)
                credentials = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
            else:
                # Use file
                credentials = service_account.Credentials.from_service_account_file(
                    self.service_account_file,
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
            
            self.service = build('calendar', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Error authenticating with Google Calendar: {e}")
            raise
    
    def set_user_access_token(self, access_token: str):
        """
        Set the service to use a user's OAuth access token
        """
        if not access_token:
            return
        try:
            credentials = Credentials(token=access_token, scopes=['https://www.googleapis.com/auth/calendar'])
            self.service = build('calendar', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Error authenticating with user access token: {e}")
            raise

    def get_upcoming_events(self, max_results: int = 10, access_token: str = "") -> List[Dict[str, Any]]:
        """
        Get upcoming calendar events
        """
        if access_token:
            self.set_user_access_token(access_token)
        if self.service is None:
            raise Exception("Google Calendar service not initialized")
            
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            end_time = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
            
            calendar_id = 'primary'
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=end_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return [
                {
                    'id': event['id'],
                    'summary': event.get('summary', 'No title'),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'description': event.get('description', ''),
                    'location': event.get('location', '')
                }
                for event in events
            ]
        except HttpError as error:
            print(f"Error getting calendar events: {error}")
            return []
    
    def create_event(self, summary: str, start_time: str, end_time: str, 
                    description: str = "", location: str = "", access_token: str = "") -> Dict[str, Any]:
        """
        Create a new calendar event
        """
        if access_token:
            self.set_user_access_token(access_token)
        if self.service is None:
            raise Exception("Google Calendar service not initialized")
            
        try:
            event = {
                'summary': summary,
                'description': description,
                'location': location,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'UTC',
                },
            }
            
            calendar_id = 'primary'
            
            event = self.service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            
            return {
                'id': event['id'],
                'summary': event['summary'],
                'start': event['start']['dateTime'],
                'end': event['end']['dateTime'],
                'description': event.get('description', ''),
                'location': event.get('location', '')
            }
        except HttpError as error:
            print(f"Error creating calendar event: {error}")
            raise
    
    def delete_event(self, event_id: str, access_token: str = "") -> bool:
        """
        Delete a calendar event
        """
        if access_token:
            self.set_user_access_token(access_token)
        if self.service is None:
            raise Exception("Google Calendar service not initialized")
            
        try:
            calendar_id = 'primary'
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            return True
        except HttpError as error:
            print(f"Error deleting calendar event: {error}")
            return False
    
    def update_event(self, event_id: str, access_token: str = "", **kwargs) -> Dict[str, Any]:
        """
        Update an existing calendar event
        """
        if access_token:
            self.set_user_access_token(access_token)
        if self.service is None:
            raise Exception("Google Calendar service not initialized")
            
        try:
            calendar_id = 'primary'
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            # Update fields if provided
            if 'summary' in kwargs:
                event['summary'] = kwargs['summary']
            if 'description' in kwargs:
                event['description'] = kwargs['description']
            if 'location' in kwargs:
                event['location'] = kwargs['location']
            if 'start_time' in kwargs:
                event['start']['dateTime'] = kwargs['start_time']
            if 'end_time' in kwargs:
                event['end']['dateTime'] = kwargs['end_time']
            
            updated_event = self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            return {
                'id': updated_event['id'],
                'summary': updated_event['summary'],
                'start': updated_event['start']['dateTime'],
                'end': updated_event['end']['dateTime'],
                'description': updated_event.get('description', ''),
                'location': updated_event.get('location', '')
            }
        except HttpError as error:
            print(f"Error updating calendar event: {error}")
            raise
    
    def find_event_by_title(self, title: str, access_token: str = "") -> Optional[Dict[str, Any]]:
        """
        Find an event by its title (case-insensitive partial match)
        """
        if access_token:
            self.set_user_access_token(access_token)
        if self.service is None:
            raise Exception("Google Calendar service not initialized")
            
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            end_time = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
            
            calendar_id = 'primary'
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=end_time,
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            title_lower = title.lower()
            
            for event in events:
                event_title = event.get('summary', '').lower()
                if title_lower in event_title or event_title in title_lower:
                    return {
                        'id': event['id'],
                        'summary': event.get('summary', 'No title'),
                        'start': event['start'].get('dateTime', event['start'].get('date')),
                        'end': event['end'].get('dateTime', event['end'].get('date')),
                        'description': event.get('description', ''),
                        'location': event.get('location', '')
                    }
            
            return None
        except HttpError as error:
            print(f"Error finding event by title: {error}")
            return None

    def get_event_by_id(self, event_id: str, access_token: str = "") -> Optional[Dict[str, Any]]:
        """
        Get a specific event by its ID
        """
        if access_token:
            self.set_user_access_token(access_token)
        if self.service is None:
            raise Exception("Google Calendar service not initialized")
            
        try:
            calendar_id = 'primary'
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            return {
                'id': event['id'],
                'summary': event.get('summary', 'No title'),
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'end': event['end'].get('dateTime', event['end'].get('date')),
                'description': event.get('description', ''),
                'location': event.get('location', '')
            }
        except HttpError as error:
            print(f"Error getting event by ID: {error}")
            return None 