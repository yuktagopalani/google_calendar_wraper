from google_auth_oauthlib.flow import InstalledAppFlow
import environ
env = environ.Env()
environ.Env.read_env()

scopes = env('SCOPES')
flow = InstalledAppFlow.from_client_secrets_file('api/client_secret.json', scopes=scopes, redirect_uri=env('AUTH_URI'))

def authenticate():
    auth_uri, state = flow.authorization_url()
    return auth_uri, state

def fetch_token(authorization_response):
    if "http:" in authorization_response:
        authorization_response = "https:" + authorization_response[5:]
    flow.fetch_token(authorization_response=authorization_response)







