from rest_framework.response import Response
from rest_framework.decorators import api_view
from api import calendar_events
from api import o_auth
from django.shortcuts import redirect
@api_view(['GET'])
def health_check(request):
    return Response(200)

@api_view(['GET'])
def google_calendar_init_view(request):
    auth_uri = o_auth.authenticate()
    return redirect(auth_uri)


@api_view(['GET'])
def google_calendar_redirect_view(request):

    return Response('its working')
