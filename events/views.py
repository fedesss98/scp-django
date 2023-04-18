from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.


class EventListView(ListView):
    model = Event


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

