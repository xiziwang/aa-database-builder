import httplib2
import os.path

from oauth2client import file
from oauth2client import tools
from oauth2client import client
from apiclient.discovery import build

SCOPES = 'https://www.googleapis.com/auth/calendar'
APPLICATION_NAME = 'AA Meeting List'
USER_AGENT = 'AA Meeting List/v1.0'
DEVELOPER_KEY='AIzaSyAQPEfdbxqgM76m3hoKQ97XzWigRMJhyjc' # from Lucy's API -> (you can change it later)
CLIENT_ID = '842246703401-h2638a17h972tqfq8c6rpqktugq765p3.apps.googleusercontent.com' # from Lucy's credentials (type other) -> (you can change it later)
CLIENT_SECRET = '8Vf32x56-3-2mmUhLeGeDgZJ' # from Lucy's credentials (type other) -> (you can change it later)

# Set up a Flow object to be used if we need to authenticate.
FLOW = client.OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPES, user_agent=USER_AGENT)

# have a path that can be used to store credentials
storage_dir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(storage_dir):
	os.makedirs(storage_dir)
storage_file = os.path.join(storage_dir, 'calendar.dat')

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
store = file.Storage(storage_file)
credentials = store.get()
if not credentials or credentials.invalid==True:
	credentials = tools.run_flow(FLOW, store)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = credentials.authorize(httplib2.Http())

# Build a service object for interacting with the API.
service = build(serviceName='calendar', version='v3', http=http, developerKey=DEVELOPER_KEY)