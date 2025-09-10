import os
import pathlib
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings
from django.shortcuts import redirect

# Path to the credentials.json
GOOGLE_CREDENTIALS_PATH = os.path.join(settings.BASE_DIR, 'credentials.json')
REDIRECT_URI = "http://localhost:8000/oauth2callback/"

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Step 1: Create a Flow object
def get_flow():
    return Flow.from_client_secrets_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

# Step 2: Build Gmail Service after getting credentials
def get_gmail_service(credentials):
    return build('gmail', 'v1', credentials=credentials)
