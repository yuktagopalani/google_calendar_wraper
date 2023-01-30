from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from django.shortcuts import redirect
from django.urls import reverse


scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file('api/client_secret.json', scopes=scopes, redirect_uri='urn:ietf:wg:oauth:2.0:oob')

def authenticate():
    auth_uri, state = flow.authorization_url()
    return auth_uri, state






