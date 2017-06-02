from __future__ import print_function

from apiclient import discovery

import datetime

import google_calendar

calendarId = 'district59aa@gmail.com' # is also the src value

# get a list of events
def getEvents(pageToken=None):
    events = google_calendar.service.events().list(
        calendarId=calendarId,
        singleEvents=True,
        maxResults=1000,
        orderBy='startTime',
        timeMin='2017-04-01T00:00:00-08:00',
        timeMax='2017-04-20T00:00:00-08:00',
        pageToken=pageToken,
        ).execute()
    return events

# print each event
def main():
    events = getEvents()
    while True:
        for event in events['items']:
            print(event)
        page_token = events.get('nextPageToken')
        if page_token:
            events = getEvents(page_token)
        else:
            break

# run the main function
if __name__ == '__main__':
    main()
