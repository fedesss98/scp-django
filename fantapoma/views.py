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


def view_athlete(request, id):
    athlete = Athlete.objects.get(id=id)
    user = request.user
    races = athlete.race_set.all()
    if user.athlete_set.filter(id=athlete.id).exists():
        buy = False
    else:
        buy = True
    context = {
        'title': f"{athlete.name} - Fantapoma",
        'athlete': athlete,
        'races': races,
        'buy': buy,
    }

    if request.method == 'GET':
        """ Mostra atleta """
        print('GET')
    elif request.method == 'POST':
        """ Prenota atleta """
        athlete.players.add(user)
        user.franchs = user.franchs - athlete.adjusted_points
        print('POST')


    return render(request, 'fantapoma/view_athlete.html', context)

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