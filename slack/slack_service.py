import os

import ssl
import certifi
from dotenv import load_dotenv
from slack_sdk import WebClient

class slack_object:
    def __init__(self, channel):
        load_dotenv()
        token = os.getenv("SLACK_TOKEN")
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = WebClient(token=token, ssl=ssl_context)
        self.channel = channel
        #github, server_log, show-gy-main, 구글일정관리
    def send_message(self, message):
        self.client.chat_postMessage(
            channel="#test",
            text=message
        )