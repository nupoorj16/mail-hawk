from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings

def get_flow():
    return Flow.from_client_secrets_file(
        settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
        scopes=['https://www.googleapis.com/auth/gmail.readonly'],
        redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI
    )

def get_gmail_service(credentials):
    return build('gmail', 'v1', credentials=credentials)
