import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def set_connection():
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, "credentials.json")
    token_path = os.path.join(current_dir, "token.json")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds

def check_mento(message):
    if "멘토" in message:
        return True

def get_calendar_result_edit(event_list):
    events = event_list.get("items", [])
    start_list = []
    event_list = []
    if not events:
        return

    for event in events:
        if check_mento(event["summary"]):
            start = event["start"].get("dateTime", event["start"].get("data"))
            start_list.append(start)
            event_list.append(event["summary"])

    return start_list, event_list

class Google_connect:
    def __init__(self,):
        self.creds = set_connection()

    def get_calendar_results(self):
        try:
            service = build("calendar", "v3", credentials=self.creds)
            now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
            events_result = (
                service.events()
                .list(
                    calendarId = "primary",
                    timeMin = now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                ).execute()
            )
            return events_result
        except HttpError as error:
            print(f"error is : {error}")

    def send_google_calendar_mento_meeting(self):
        meeting_list = self.get_calendar_results()
        mento_meeting_start_list, mento_meeting_list = get_calendar_result_edit(meeting_list)

        return mento_meeting_start_list, mento_meeting_list
