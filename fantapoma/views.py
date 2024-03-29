from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import F

from django.contrib.auth.mixins import LoginRequiredMixin

from fantapoma.models import FantaAthlete, Special
from django.contrib.auth.models import User
from .forms import UpdatePointsForm

from django.contrib import messages


def index(request):
    # return HttpResponse("Fantapoma")
    return render(request, 'fantapoma/index.html', {
        'title': 'Fantapoma: - Il gioco di canottaggio virtuale',
        'nav-home': 'active'})


def view_athlete(request, id):
    fantaathlete = FantaAthlete.objects.get(id=id)
    user = request.user
    if fantaathlete.athlete is not None:
        # All the crews of all the races in which the athlete has participated
        crews = fantaathlete.athlete.crew_set.all() 
        # All the races in which the athlete has participated
        races = [crew.race for crew in crews]
    else:
        races = []
    buy = True
    sell = False
    # If the user has the athlete in it's eight
    if user.athletes_set.filter(id=fantaathlete.id).exists():
        # Cannot buy, can sell
        buy = False
        sell = True
    # If the user doesn't have the player
    # and doesn't have franchs or doesn't have more space
    elif (user.player.franchs <= 0 
          or user.athletes_set.count() >= 8):
        # Cannot buy, cannot sell
        buy = False
        sell = False
    context = {
        'title': f"{fantaathlete.name} - Fantapoma",
        'athlete': fantaathlete,
        'races': races,
        'buy': buy,
        'sell': sell,
    }

    if request.method == 'POST':
        """ Prenota atleta """
        if 'acquista' in request.POST:
            franchs = fantaathlete.adjusted_price
            remain_franchs = user.player.franchs - franchs
            if remain_franchs >= 0:
                print('Acquista')
                fantaathlete.players.add(user)
                fantaathlete.save()
                user.player.franchs = remain_franchs
                # Now user cannot buy but can sell
                context['buy'] = False
                context['sell'] = True
                messages.success(request, 'Acquistato!')
            else:
                messages.error(request, 'Non hai abbastanza Franchini per comprare!')
        elif 'rimuovi' in request.POST:
            fantaathlete.players.remove(user)
            franchs = fantaathlete.adjusted_price
            fantaathlete.save()
            user.player.franchs = user.player.franchs + franchs
            # Now user can buy but cannot sell
            context['buy'] = True
            context['sell'] = False
        request.user.player.save()
    return render(request, 'fantapoma/view_athlete.html', context)


class MyCrewView(LoginRequiredMixin, ListView):
    model = FantaAthlete
    template_name = "fantapoma/mycrew.html"

    context_object_name = 'player'

    def get_queryset(self):
        self.user = self.request.user
        return self.user.athletes_set.all()

    def get_context_data(self, **kwargs):
        self.user = self.request.user
        context = super().get_context_data(**kwargs)
        context['atleti'] = self.user.athletes_set.all()
        return context


# MARKETPLACE
class FantaAthleteView(ListView):
    template_name = "fantapoma/marketplace.html"
    model = FantaAthlete
    ordering = '-name'

    def get_queryset(self):
        athlete_name = self.request.GET.get('athlete_name')
        print(athlete_name)
        queryset = super().get_queryset().order_by('name')
        if athlete_name is not None:
            queryset = FantaAthlete.objects.filter(name__icontains=athlete_name)
        print(queryset)
        return queryset
    
    def get_ordering(self):
        increasing = self.request.GET.get('increasing', 'off')
        ordering = self.request.GET.get('order', 'name')
        if increasing != 'on':
            ordering = '-' + ordering
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.user = self.request.user
        atlethes = self.user.athletes_set.all().values_list('name', flat=True)
        context['atleti'] = list(atlethes)
        context['ordering'] = self.request.GET.get('order', 'name')
        context['increasing'] = self.request.GET.get('increasing', 'off')
        return context

class LeaderboardView(ListView):
    model = User
    template_name = 'fantapoma/leaderboard.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return sorted(queryset, key=lambda u: u.player.score, reverse=True)

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

        context['athletes'] = FantaAthlete.objects.filter(players__pk=pk)
        return context

    
class CreateSpecialView(CreateView):
    model = Special
    fields = '__all__'


class ListSpecialsView(ListView):
    model = Special


class RawFantaAthleteListView(ListView):
    model = FantaAthlete
    template_name = 'fantapma/athlete_list.html'


class UpdatePointsView(LoginRequiredMixin, FormView):
    template_name = 'fantapoma/submit_points.html'
    form_class = UpdatePointsForm
    success_url = reverse_lazy('leaderboard')

    def handle_no_permission(self):
        # Update an error message befor redirecting
        messages.error(self.request, 'Devi fare il login prima di aggiungere il tuo punteggio')
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        # Update the context data to serve the name of the athlete selected by URL ID
        context = super().get_context_data(**kwargs)
        athlete_id = self.kwargs.get('athlete_id')
        if athlete_id:
            athlete = FantaAthlete.objects.get(id=athlete_id)
            context['athlete'] = athlete.name
        return context

    def get_form_kwargs(self):
        # Takes the user athlete or one athlete with ID specified in the URL 
        kwargs = super().get_form_kwargs()
        athlete_id = self.kwargs.get('athlete_id')
        if athlete_id:
            athlete = FantaAthlete.objects.get(id=athlete_id)
        else:
            athlete = self.request.user.true_athlete
        kwargs['instance'] = athlete
        return kwargs

    def form_valid(self, form):
        # Save the updated model
        # form.instance = self.request.user.athlete
        form.save()
        return super().form_valid(form)
    
class EventsView(TemplateView):
    template_name = 'fantapoma/../events/templates/events/events.html'


class StatisticsView(TemplateView):
    template_name = 'fantapoma/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_athletes = FantaAthlete.objects.annotate(
            points_sum=F('race_points') + F('actions_points')
        ).order_by('-points_sum')[:5]
        top_race_athletes = FantaAthlete.objects.order_by('-race_points')[:5]
        top_actions_athletes = FantaAthlete.objects.order_by('-actions_points')[:5]
        context['best_athlete'] = top_athletes[0] 
        context['top_athletes'] = top_athletes
        context['race_points'] = [athlete.race_points for athlete in top_athletes]
        context['actions_points'] = [athlete.actions_points for athlete in top_athletes]
        context['top_race_athletes'] = top_race_athletes
        context['top_actions_athletes'] = top_actions_athletes
        return context