from django.urls import path
from base import views

urlpatterns = [
    path('init', views.google_calendar_init_view),
    path('redirect',views.google_calendar_redirect_view)
]


