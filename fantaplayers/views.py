from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate

from fantapoma.models import Player
from fantaplayers.forms import PlayerCreationForm

# Create your views here.

class CreatePlayer(CreateView):
    model = User
    form_class = PlayerCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('fantapoma')

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

class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Player
    fields = ['team_name']
    initial = {}

    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('mycrew')
