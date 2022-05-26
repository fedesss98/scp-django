from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from fantapoma.models import Athlete
from django.contrib.auth.models import User

from django.contrib import messages

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
        print(f"{request.user.player} has {request.user.player.franchs}")
    elif request.method == 'POST':
        """ Prenota atleta """
        if 'acquista' in request.POST:
            print('Acquista')
            franchs = athlete.adjusted_points
            athlete.players.add(user)
            print(f'{franchs} + {request.user.player.franchs}')
            athlete.save()
            request.user.player.franchs = request.user.player.franchs - franchs
            context['buy'] = False
        elif 'rimuovi' in request.POST:
            print('Rimuovi')
            athlete.players.remove(user)
            franchs = athlete.adjusted_points
            print(f'{franchs} + {request.user.player.franchs}')
            athlete.save()
            request.user.player.franchs = request.user.player.franchs + franchs
            context['buy'] = True
        request.user.player.save()
        print(f"{request.user.player} has {request.user.player.franchs}")


    return render(request, 'fantapoma/view_athlete.html', context)

class MyCrewView(LoginRequiredMixin, ListView):
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