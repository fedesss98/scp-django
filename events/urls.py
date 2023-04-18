from django.urls import include, path

from events.views import *

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='list-events'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
]
