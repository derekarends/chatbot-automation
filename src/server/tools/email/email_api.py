import json
import os.path
import pickle
import base64
import email
from email.mime.text import MIMEText
from pydantic.v1 import BaseModel, Extra, root_validator
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from langchain.utils import get_from_dict_or_env

from .email_prompts import (
    Modes,
    SEARCH_EMAIL_FROM,
    SEND_EMAIL,
    SEARCH_EMAIL_SUBJECT,
)


class EmailApiWrapper(BaseModel):
    """ Wrapper for reading and sending emails. """
    SCOPES = ['https://mail.google.com/']
    credentials: str = None

    operations: list[dict] = [
        {
            "mode": Modes.SEARCH_EMAIL_FROM,
            "name": "Read an email from an email address",
            "description": SEARCH_EMAIL_FROM,
        },
        {
            "mode": Modes.SEND_EMAIL,
            "name": "Send an email to an email address",
            "description": SEND_EMAIL,
        },
        {
            "mode": Modes.SEARCH_EMAIL_SUBJECT,
            "name": "Search for an email based on subject",
            "description": SEARCH_EMAIL_SUBJECT,
        }
    ]

    class Config:
        """ Configuration for this pydantic object. """
        extra = Extra.forbid
        arbitrary_types_allowed = True

    def list_operations(self) -> list[dict]:
        return self.operations

    @root_validator(pre=True)
    def validate_env(cls, data: dict) -> dict:
        """ Validate the environment variables. """

        creds = get_from_dict_or_env(data, "credentials", "CREDENTIALS")
        data["credentials"] = creds

        return data

    def run(self, mode: str, text: str | None) -> str:
        """ Based on the mode from the caller, run the appropriate function. """
        if mode == Modes.SEARCH_EMAIL_FROM:
            return self.read_email_from(text)
        elif mode == Modes.SEND_EMAIL:
            return self.send_email(text)
        elif mode == Modes.SEARCH_EMAIL_SUBJECT:
            return self.search_email_subject(text)
        else:
            raise ValueError(f"Got unexpected mode {mode}")

    def search_email_subject(self, subject: str) -> list[dict]:
        """ Search for emails with subject line. """
        data = json.loads(subject)
        return self.read_messages(f"subject:{data['subject']}")

    def read_email_from(self, from_address: str) -> list[dict]:
        """ Read an email from an email address. """
        data = json.loads(from_address)
        return self.read_messages(f"from:{data['from']}")

    def read_messages(self, query: str) -> list[dict]:
        """ Read messages from an email address. """
        try:
            service = self._build()

            # request a list of all the messages
            result = service.users().messages().list(
                maxResults='100', userId='me', q=query).execute()
            messages = result.get('messages')

            to_return: list[dict] = []

            # iterate through all the messages
            for msg in messages:
                raw_msg = service.users().messages().get(
                    userId='me', id=msg['id'], format='raw').execute()
                mime_msg = email.message_from_bytes(
                    base64.urlsafe_b64decode(raw_msg['raw']))

                subject = mime_msg['subject']
                body = ""

                message_main_type = mime_msg.get_content_maintype()
                if message_main_type == 'multipart':
                    for part in mime_msg.get_payload():
                        if part.get_content_maintype() == 'text':
                            body = f"{body} {part.get_payload()}"
                            break
                elif message_main_type == 'text':
                    body = mime_msg.get_payload()

                to_return.append({"subject": subject, "body": body})

        except Exception as e:
            print(e)
            raise Exception("Failed to read emails")

        return to_return

    def send_email(self, text: str) -> str:
        """ Send an email to an email address. """
        try:
            service = self._build()

            data = json.loads(text)

            message = MIMEText(data['body'])
            message['to'] = data['to']
            message['subject'] = data['subject']
            encoded_message = {'raw': base64.urlsafe_b64encode(
                message.as_bytes()).decode()}

            message = service.users().messages().send(
                userId="me", body=encoded_message).execute()
            print(F'sent message to {message} Message Id: {message["id"]}')
        except Exception as e:
            print(e)
            raise Exception("Failed to send email")

    def _build(self):

        # Variable creds will store the user access token.
        # If no valid token found, we will create one.
        creds = None

        # The file token.pickle contains the user access token.
        # Check if it exists
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If credentials are not available or are invalid, ask the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    json.loads(self.credentials), self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle file for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # Connect to the Gmail API
        return build('gmail', 'v1', credentials=creds)
