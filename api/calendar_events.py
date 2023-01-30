from . import o_auth
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
from googleapiclient.errors import HttpError
import os
def get_calendar_events():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', o_auth.scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = o_auth.flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return 'No upcoming events found.'

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        return events

    except HttpError as error:
        print('An error occurred: %s' % error)
        return error











    # flow = InstalledAppFlow.from_client_secrets_file('api/client_secret.json', scopes=scopes
    # service = o_auth.authenticate()
    # calendar_info = service.calendarList().list().execute()
    # calendar_id = calendar_info['items'][0]['id']
    # time_zone = calendar_info['items'][0]['timeZone']
    # result = service.events().list(calendarId=calendar_id, timeZone=time_zone).execute()
    # events = result['items']
    # return events
