from __future__ import print_function
import os.path
import base64
from email import message_from_bytes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_recent_emails(service, max_results=5):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload.get('headers')
        subject = [i['value'] for i in headers if i['name'] == 'Subject']
        parts = payload.get('parts')
        body = ""
        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    data = data.replace("-", "+").replace("_", "/")
                    decoded_data = base64.b64decode(data)
                    body += decoded_data.decode()
        emails.append({
            'subject': subject[0] if subject else "(No Subject)",
            'body': body
        })
    return emails
def search_emails_by_sender(service, sender_email, max_results=5):
    """
    Search emails by sender's email address and return top emails.
    """
    results = service.users().messages().list(
        userId='me',
        q=f'from:{sender_email}',
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload.get("headers")
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')

        # Extract snippet as content preview
        snippet = txt.get('snippet', '')

        emails.append({
            'subject': subject,
            'snippet': snippet
        })

    return emails

