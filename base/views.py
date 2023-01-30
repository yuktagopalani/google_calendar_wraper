from rest_framework.response import Response
from rest_framework.decorators import api_view
from api import calendar_events, o_auth
from api import o_auth
from django.shortcuts import redirect
from google_auth_oauthlib.flow import InstalledAppFlow
import environ
env = environ.Env()
environ.Env.read_env()

@api_view(['GET'])
def health_check(request):
    return Response(200)

@api_view(['GET'])
def google_calendar_init_view(request):
    auth_uri, state = o_auth.authenticate()
    o_auth.flow.redirect_uri = env('REDIRECT_URI')
    request.session['state'] = state
    return redirect(auth_uri)



@api_view(['GET'])
def google_calendar_redirect_view(request):
    state = request.session['state']
    o_auth.flow = InstalledAppFlow.from_client_secrets_file('api/client_secret.json', scopes=o_auth.scopes, redirect_uri=env('REDIRECT_URI'), state=state)
    authorization_response = request.build_absolute_uri()
    o_auth.fetch_token(authorization_response)
    events = calendar_events.get_calendar_events()
    return Response(events)




