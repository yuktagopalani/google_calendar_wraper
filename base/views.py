from rest_framework.response import Response
from rest_framework.decorators import api_view
from api import calendar_events, o_auth
from api import o_auth
from django.shortcuts import redirect
from rest_framework import status
from apiclient.discovery import build
import pickle
import json

from google_auth_oauthlib.flow import InstalledAppFlow
@api_view(['GET'])
def health_check(request):
    return Response(200)

@api_view(['GET'])
def google_calendar_init_view(request):
    # o_auth.flow.redirect_uri = 'http://127.0.0.1:8000/profiles/oauth2callback/'
    #
    # o_auth.flow.fetch_token(code=request.GET.get('code'))
    #
    # service = build("calendar", "v3", credentials=o_auth.flow.credentials)
    #
    # return redirect('http://127.0.0.1:8000/rest/v1/calendar/redirect/')
    auth_uri, state = o_auth.authenticate()
    o_auth.flow.redirect_uri = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'
    request.session['state'] = state
    return redirect(auth_uri)
    # o_auth.flow.fetch_token(code=request.GET.get('code'))
    # service = build("calendar", "v3", credentials=o_auth.flow.credentials)
    # result = service.calendarList().list().execute()
    # return Response(result['items'][0])


@api_view(['GET'])
def google_calendar_redirect_view(request):
    state = request.session['state']
    o_auth.flow = InstalledAppFlow.from_client_secrets_file('api/client_secret.json', scopes=o_auth.scopes, redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect', state=state)
    authorization_response = request.build_absolute_uri()
    if "http:" in authorization_response:
        authorization_response = "https:" + authorization_response[5:]
    print(authorization_response)
    o_auth.flow.fetch_token(authorization_response=authorization_response)
    service = build("calendar", "v3", credentials=o_auth.flow.credentials)
    calendar_info = service.calendarList().list().execute()
    calendar_id = calendar_info['items'][0]['id']
    time_zone = calendar_info['items'][0]['timeZone']
    result = service.events().list(calendarId=calendar_id, timeZone=time_zone).execute()
    events = result['items']
    return Response(events)

    # The credentials are available in flow.credentials, not the return value
    # service = build(API_SERVICE_NAME, API_VERSION, credentials=flow.credentials)
    # pickle.dump(credentials, open("token.pkl", "wb"))
    # credentials = pickle.load(open("token.pkl", "rb"))
    # token = json.dumps(response)
    # with open("token.json", "w") as outfile:
    #     outfile.write(token)
    # events = calendar_events.get_calendar_events()
    # return Response(events)



