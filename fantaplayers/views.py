from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy

from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate

from fantapoma.models import FantaAthlete, Player
from fantaplayers.forms import PlayerCreationForm

# Create your views here.


class CreatePlayer(CreateView):
    model = User
    form_class = PlayerCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('fantapoma:index')

    def form_valid(self, form):
        form.save()
        #authenticate user then login
        username=form.cleaned_data['username']
        password=form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        print(f'Form is valid: {form.instance}\n {username} - {password}')
        return redirect(self.success_url)


class ProfileView(LoginRequiredMixin, CreateView):
    model = Player
    fields = ['team_name']
    template_name = 'fantaplayers/profile.html'

    
    def post(self, request, *args, **kwargs):
        cox_id = request.POST.get('cox')
        cox = get_object_or_404(FantaAthlete, id=cox_id)
        request.user.player.cox = cox
        request.user.player.save()
        return HttpResponseRedirect(reverse('fantapoma:mycrew'))




class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Player
    fields = ['team_name']
    initial = {}

    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('fantapoma:mycrew')
