from django.shortcuts import render

from django.views.generic import ListView
from .models import Event

# Create your views here.


class EventListView(ListView):
    model = Event

