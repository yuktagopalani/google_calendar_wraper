from . import o_auth

def get_calendar_events():
    service = o_auth.authenticate()
    calendar_info = service.calendarList().list().execute()
    calendar_id = calendar_info['items'][0]['id']
    time_zone = calendar_info['items'][0]['timeZone']
    result = service.events().list(calendarId=calendar_id, timeZone=time_zone).execute()
    events = result['items']
    return events
