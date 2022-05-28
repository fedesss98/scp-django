from math import remainder
from urllib import request
from urllib.parse import non_hierarchical
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
    if (user.athlete_set.filter(id=athlete.id).exists() 
        or user.player.franchs <= 0
        or user.athlete_set.count() >= 8):
        buy = False
    else:
        buy = True
    context = {
        'title': f"{athlete.name} - Fantapoma",
        'athlete': athlete,
        'races': races,
        'buy': buy,
    }

    if request.method == 'POST':
        """ Prenota atleta """
        if 'acquista' in request.POST:
            franchs = athlete.adjusted_points
            remain_franchs = user.player.franchs - franchs
            if remain_franchs >= 0:
                print('Acquista')
                athlete.players.add(user)
                athlete.save()
                user.player.franchs = remain_franchs
                context['buy'] = False
                messages.success(request, 'Acquistato!')
            else:
                messages.error(request, 'Non hai abbastanza Franchini per comprare!')
        elif 'rimuovi' in request.POST:
            athlete.players.remove(user)
            franchs = athlete.points
            athlete.save()
            user.player.franchs = user.player.franchs + franchs
            context['buy'] = True
        request.user.player.save()


    return render(request, 'fantapoma/view_athlete.html', context)

class MyCrewView(LoginRequiredMixin, ListView):
    model = Athlete
    template_name = "fantapoma/mycrew.html"

    context_object_name = 'player'

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

    def get_queryset(self):
        athlete_name = self.request.GET.get('athlete_name') 
        if athlete_name is not None:
            self.queryset = Athlete.objects.filter(name__contains=athlete_name)
        else:
            self.queryset = Athlete.objects.all()
        return super().get_queryset()
    
    def get_ordering(self):
        increasing = self.request.GET.get('increasing', 'off')
        ordering = self.request.GET.get('order', 'name')
        if increasing != 'on':
            ordering = '-' + ordering
        print(ordering)
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.user = self.request.user
        atlethes = self.user.athlete_set.all().values_list('name', flat=True)
        context['atleti'] = list(atlethes)
        context['ordering'] = self.request.GET.get('order', 'name')
        context['increasing'] = self.request.GET.get('increasing', 'off')
        return context

class LeaderboardView(ListView):
    model = User
    template_name = 'fantapoma/leaderboard.html'

    context_object_name = 'players'


class ViewCrew(DetailView):
    model = User
    template_name = 'fantapoma/view_crew.html'

    context_object_name = 'player'

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is None:
            pk = self.request.user.id
            self.kwargs[self.pk_url_kwarg] = pk
        return super(ViewCrew, self).get_object()         

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is None:
            pk = self.request.user.id

        context['athletes'] = Athlete.objects.filter(players__pk=pk)
        return context