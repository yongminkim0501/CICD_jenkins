import sys
import datetime

from topic.google_calendar.google_main import Google_connect
from slack_service import slack_object

def format_datetime(iso_string):
    """ISO 형식을 읽기 쉬운 형식으로 변환"""
    dt = datetime.datetime.fromisoformat(iso_string)
    return dt.strftime("%Y년 %m월 %d일 %H:%M")

def main():
    google = Google_connect()
    start_list, meeting_list = google.send_google_calendar_mento_meeting()
    result = []
    for idx in range(len(meeting_list)):
        result.append(f"시간은 : {format_datetime(start_list[idx])}, 내용은 : {meeting_list[idx]}")
    slack = slack_object("#구글일정관리")
    slack.send_message(result[0])

if __name__ == "__main__":
    main()