from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django import forms 

from django.contrib.auth.mixins import LoginRequiredMixin

from fantapoma.models import Athlete, Special
from django.contrib.auth.models import User
from .forms import UpdatePointsForm

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
    buy = True
    sell = False
    # If the user has the athlete in it's eight
    if user.athlete_set.filter(id=athlete.id).exists():
        # Cannot buy, can sell
        buy = False
        sell = True
    # If the user doesn't have the player
    # and doesn't have franchs or doesn't have more space
    elif (user.player.franchs <= 0 
          or user.athlete_set.count() >= 8):
        # Cannot buy, cannot sell
        buy = False
        sell = False
    context = {
        'title': f"{athlete.name} - Fantapoma",
        'athlete': athlete,
        'races': races,
        'buy': buy,
        'sell': sell,
    }

    if request.method == 'POST':
        """ Prenota atleta """
        if 'acquista' in request.POST:
            franchs = athlete.adjusted_price
            remain_franchs = user.player.franchs - franchs
            if remain_franchs >= 0:
                print('Acquista')
                athlete.players.add(user)
                athlete.save()
                user.player.franchs = remain_franchs
                # Now user cannot buy but can sell
                context['buy'] = False
                context['sell'] = True
                messages.success(request, 'Acquistato!')
            else:
                messages.error(request, 'Non hai abbastanza Franchini per comprare!')
        elif 'rimuovi' in request.POST:
            athlete.players.remove(user)
            franchs = athlete.adjusted_price
            athlete.save()
            user.player.franchs = user.player.franchs + franchs
            # Now user can buy but cannot sell
            context['buy'] = True
            context['sell'] = False
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


# MARKETPLACE
class AthleteView(ListView):
    template_name = "fantapoma/marketplace.html"
    model = Athlete

    def get_queryset(self):
        athlete_name = self.request.GET.get('athlete_name') 
        if athlete_name is not None:
            self.queryset = Athlete.objects.filter(name__icontains=athlete_name)
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

    context_object_name = 'users'


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

    
class CreateSpecialView(CreateView):
    model = Special
    fields = '__all__'


class ListSpecialsView(ListView):
    model = Special


class RawAthleteListView(ListView):
    model = Athlete
    template_name = 'fantapma/athlete_list.html'


class UpdatePointsView(FormView):
    template_name = 'fantapoma/submit_points.html'
    form_class = UpdatePointsForm
    success_url = reverse_lazy('leaderboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        athlete_id = self.kwargs.get('athlete_id')
        if athlete_id:
            kwargs['initial']['athlete_id'] = athlete_id
        return kwargs

    def form_valid(self, form):
        athlete_id = form.cleaned_data.get('athlete_id')
        if athlete_id:
            athlete = get_object_or_404(Athlete, id=athlete_id)
            form.instance = athlete
        else:
            form.instance = self.request.user.athlete
        form.save()
        return super().form_valid(form)