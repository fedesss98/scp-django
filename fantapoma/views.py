from pyexpat import model
from re import template
from typing import List
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.generic import ListView

from fantapoma.models import Athlete, Player

def index(request):
    #return HttpResponse("Fantapoma")
    return render(request, 'fantapoma/index.html', {
        'title': 'Fantapoma: - Il gioco di canottaggio virtuale',
        'nav-home': 'active'})

class MyCrewView(ListView):
    template_name = "fantapoma/mycrew.html"

    def get_queryset(self):
        self.user = self.request.user
        return self.user.athlete_set.all()

    def get_context_data(self, **kwargs):
        self.user = self.request.user
        context = super().get_context_data(**kwargs)
        context['atleti'] = self.user.athlete_set.all()
        return context

class AthleteView(ListView):
    template_name = "fantapoma/marketplace.html"
    model = Athlete
    
    def get_context_data(self, **kwargs):
        self.user = self.request.user
        context = super().get_context_data(**kwargs)
        atlethes = self.user.athlete_set.all().values_list('name', flat=True)
        context['atleti'] = list(atlethes)
        return context