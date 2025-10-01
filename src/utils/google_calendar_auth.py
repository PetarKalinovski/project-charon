import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for google calendar API
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar",
]


def authenticate_calendar():
    creds = None
    if os.path.exists("google_credentials.json"):
        creds = Credentials.from_authorized_user_file("google_credentials.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("google_credentials.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)
