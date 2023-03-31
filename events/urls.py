from django.urls import include, path

from events.views import EventListView

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='list-events'),
]
