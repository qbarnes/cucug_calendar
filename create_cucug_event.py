#! /usr/bin/env python3
#
# Create a reoccurring event for CUCUG board meeting which is the
# first Tuesday after the 3rd Thursday.
#

import sys
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    event = {
        'summary': "CUCUG Board Meeting",
        'location': "Kevin's house.",
        'description': "CUCUG Board Meeting",
        'start': {
            'dateTime': "2023-01-24T19:00:00",
            'timeZone': "America/Chicago",
        },
        'end': {
            'dateTime': "2023-01-24T20:00:00",
            'timeZone': "America/Chicago",
        },
	# See RFC5545 (https://tools.ietf.org/html/rfc5545).
        'recurrence': [
            'RRULE:FREQ=MONTHLY;BYDAY=TU;BYMONTHDAY=20,21,22,23,24,25,26'
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 120},
                {'method': 'popup', 'minutes': 20},
            ],
        },
    }

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        event_result = service.events().insert(calendarId='primary',
            body=event).execute()

        print("created event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    except HttpError as error:
        print('An error occurred: %s' % error)

    return 0


if __name__ == '__main__':
    sys.exit(main())
